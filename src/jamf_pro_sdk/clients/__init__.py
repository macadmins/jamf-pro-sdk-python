import concurrent.futures
import logging
import tempfile
from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict, Iterable, Iterator, Optional, Type, Union
from urllib.parse import urlunparse

import certifi
import requests
import requests.adapters
from pydantic import BaseModel
from requests.utils import cookiejar_from_dict

from ..clients.classic_api import ClassicApi
from ..clients.jcds2 import JCDS2
from ..clients.pro_api import ProApi
from ..models.classic import ClassicApiModel
from ..models.client import SessionConfig
from .auth import CredentialsProvider

logger = logging.getLogger("jamf_pro_sdk")


class JamfProClient:
    def __init__(
        self,
        server: str,
        credentials: CredentialsProvider,
        port: int = 443,
        session_config: Optional[SessionConfig] = None,
    ):
        """The base client class for interacting with the Jamf Pro APIs.

        Classic API, Pro API, and JCDS2 clients are instantiated with the base client.

        If the ``aws`` extra dependency is not installed the JCDS2 client will not be created.

        :param server: The hostname of the Jamf Pro server to connect to.
        :type server: str

        :param credentials: Accepts any credentials provider object to provide the
            username and password for initial authentication.
        :type credentials: CredentialsProvider

        :param port: The server port to connect over (defaults to `443`).
        :type port: int

        :param session_config: Pass a `SessionConfig` to configure session options.
        :type session_config: SessionConfig
        """
        self.session_config = SessionConfig() if not session_config else session_config

        self._credentials = credentials
        self._credentials.attach_client(self)
        self.get_access_token = self._credentials.get_access_token

        self.base_server_url = urlunparse(
            (
                self.session_config.scheme,
                f"{server}:{port}",
                "",
                None,
                None,
                None,
            )
        )

        self.session = self._setup_session()

        self.classic_api = ClassicApi(self.classic_api_request, self.concurrent_api_requests)
        self.pro_api = ProApi(self.pro_api_request, self.concurrent_api_requests)

        try:
            self.jcds2 = JCDS2(self.classic_api, self.pro_api, self.concurrent_api_requests)
        except ImportError:
            pass

    @staticmethod
    def _parse_cookie_file(cookie_file: Union[str, Path]) -> dict[str, str]:
        """Parse a cookies file and return a dictionary of key value pairs."""
        cookies = {}
        with open(cookie_file, "r") as fp:
            for line in fp:
                if line.startswith("#HttpOnly_"):
                    fields = line.strip().split()
                    cookies[fields[5]] = fields[6]
        return cookies

    @staticmethod
    def _load_ca_cert_bundle(ca_cert_bundle_path: Union[str, Path]):
        """Create a copy of the certifi trust store and append the passed CA cert bundle in a
        temporary file.
        """
        with open(certifi.where(), "r") as f_obj:
            current_ca_cert = f_obj.read()

        with open(ca_cert_bundle_path, "r") as f_obj:
            ca_cert_bundle = f_obj.read()

        temp_ca_cert_dir = tempfile.mkdtemp(prefix="jamf-pro-sdk-")
        temp_ca_cert = f"{temp_ca_cert_dir}/cacert.pem"

        with open(temp_ca_cert, "w") as f_obj:
            f_obj.write(current_ca_cert)
            f_obj.write(ca_cert_bundle)

        return temp_ca_cert

    def _setup_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {"Accept": "application/json", "User-Agent": self.session_config.user_agent}
        )

        if self.session_config.cookie:
            cookiejar_from_dict(
                cookie_dict=self._parse_cookie_file(self.session_config.cookie),
                cookiejar=session.cookies,
            )

        if self.session_config.verify and self.session_config.ca_cert_bundle is not None:
            session.verify = self._load_ca_cert_bundle(self.session_config.ca_cert_bundle)
        else:
            session.verify = self.session_config.verify

        adapter = requests.adapters.HTTPAdapter(
            max_retries=self.session_config.max_retries,
            pool_connections=self.session_config.max_concurrency,
            pool_maxsize=self.session_config.max_concurrency,
        )
        session.mount(prefix="http://", adapter=adapter)
        session.mount(prefix="https://", adapter=adapter)

        return session

    def classic_api_request(
        self,
        method: str,
        resource_path: str,
        data: Optional[Union[str, ClassicApiModel]] = None,
        override_headers: Optional[dict] = None,
    ) -> requests.Response:
        """Perform a request to the Classic API.

        :param method: The HTTP method. Allowed values (case-insensitive) are: GET, POST,
            PUT, and DELETE.
        :type method: str

        :param resource_path: The path of the API being requested that comes `after`
            ``JSSResource``.
        :type resource_path: str

        :param data: If the request is a ``POST`` or ``PUT``, the XML string or
            ``ClassicApiModel`` that is being sent.
        :type data: str | ClassicApiModel

        :param override_headers: A dictionary of key-value pairs that will be set as
            headers for the request. You cannot override the ``Authorization`` or
            ``Content-Type`` headers.
        :type override_headers: Dict[str, str]

        :return: `Requests Response <https://requests.readthedocs.io/en/latest/api/#requests.Response>`_ object
        :rtype: requests.Response
        """
        capi_req: Dict[str, Any]

        capi_req = {
            "method": method,
            "url": f"{self.base_server_url}/JSSResource/{resource_path}",
            "headers": {"Authorization": f"Bearer {self._credentials.get_access_token()}"},
            "timeout": self.session_config.timeout,
        }

        if override_headers:
            capi_req["headers"].update(override_headers)

        if data and (method.lower() in ("post", "put")):
            capi_req["headers"]["Content-Type"] = "text/xml"
            capi_req["data"] = data if isinstance(data, str) else data.xml(exclude_read_only=True)

        with self.session.request(**capi_req) as capi_resp:
            logger.info("ClassicAPIRequest %s %s", method.upper(), resource_path)
            try:
                capi_resp.raise_for_status()
            except requests.HTTPError:
                # TODO: XML error response parser
                logger.error(capi_resp.text)
                raise

            return capi_resp

    def pro_api_request(
        self,
        method: str,
        resource_path: str,
        query_params: Optional[Dict[str, str]] = None,
        data: Optional[Union[dict, BaseModel]] = None,
        files: Optional[dict[str, tuple[str, BinaryIO, str]]] = None,
        override_headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Perform a request to the Pro API.

        :param method: The HTTP method. Allowed values (case-insensitive) are: GET, POST,
            PUT, PATCH, and DELETE.
        :type method: str

        :param resource_path: The path of the API being requested that comes `after`
            ``api``. Include the API version at the beginning of the resource path.
        :type resource_path: str

        :param query_params: Query string parameters to be included with the request URL string.
        :type query_params: Dict[str, str]

        :param data: If the request is a ``POST``, ``PUT``, or ``PATCH``, the dictionary
            or ``BaseModel`` that is being sent.
        :type data: dict | BaseModel

        :param files: If the request is a ``POST``, a dictionary with a single ``files`` key,
            and a tuple containing the filename, file-like object to upload, and mime type.
        :type files: Optional[dict[str, tuple[str, BinaryIO, str]]]

        :param override_headers: A dictionary of key-value pairs that will be set as
            headers for the request. You cannot override the ``Authorization`` or
            ``Content-Type`` headers.
        :type override_headers: Dict[str, str]

        :return: `Requests Response <https://requests.readthedocs.io/en/latest/api/#requests.Response>`_ object
        :rtype: requests.Response
        """
        pro_req: Dict[str, Any]

        pro_req = {
            "method": method,
            "url": f"{self.base_server_url}/api/{resource_path}",
            "headers": {"Authorization": f"Bearer {self._credentials.get_access_token()}"},
            "timeout": self.session_config.timeout,
        }

        if override_headers:
            pro_req["headers"].update(override_headers)

        if query_params:
            pro_req["params"] = query_params

        if data and (method.lower() in ("post", "put", "patch")):
            pro_req["headers"]["Content-Type"] = "application/json"
            if isinstance(data, dict):
                pro_req["json"] = data
            elif isinstance(data, BaseModel):
                pro_req["data"] = data.model_dump_json(exclude_none=True)
            else:
                raise ValueError("'data' must be one of 'dict' or 'BaseModel'")

        if files and (method.lower() == "post"):
            pro_req["files"] = files

        with self.session.request(**pro_req) as pro_resp:
            logger.info("ProAPIRequest %s %s", method.upper(), resource_path)
            try:
                pro_resp.raise_for_status()
            except requests.HTTPError:
                logger.error(pro_resp.text)
                raise

            return pro_resp

    def concurrent_api_requests(
        self,
        handler: Callable,
        arguments: Iterable[Any],
        return_model: Optional[Type[BaseModel]] = None,
        max_concurrency: Optional[int] = None,
        return_exceptions: Optional[bool] = None,
    ) -> Iterator[Union[Any, Exception]]:
        """An interface for performing concurrent API operations.

        :param handler: The method that will be called.
        :type handler: Callable

        :param arguments: An iterable object containing the arguments to be passed to the
            ``handler``. If the items within the iterable are dictionaries (``dict``) they
            will be unpacked when passed. Use this to pass multiple arguments.
        :type arguments: Iterable[Any]

        :param return_model: The Pydantic model that should be instantiated from the responses. The
            model will only be returned if the response from the ``handler`` is not also a model. If
            it is the ``return_model`` is ignored. The response MUST be a JSON body for this option
            to succeed.
        :type return_model: BaseModel

        :param max_concurrency: An override the value for ``session_config.max_concurrency``. Note:
            this override `cannot` be higher than ``session_config.max_concurrency``.
        :type max_concurrency: int

        :param return_exceptions: If an exception is encountered by the ``handler`` the
            iterator will continue without a yield. Setting this to ``True`` will return the
            exception object. If not set, the value for ``session_config.return_exceptions`` is
            used.
        :type return_exceptions: bool

        :return: An iterator that will yield the result for each operation.
        :rtype: Iterator

        """
        if return_exceptions is None:
            return_exceptions = self.session_config.return_exceptions

        if max_concurrency:
            max_concurrency = min(max_concurrency, self.session_config.max_concurrency)
        else:
            max_concurrency = self.session_config.max_concurrency

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrency) as executor:
            logger.info("ConcurrentAPIRequest %s ", handler.__name__)
            executor_results = list()
            for i in arguments:
                if isinstance(i, dict):
                    executor_results.append(executor.submit(handler, **i))
                else:
                    executor_results.append(executor.submit(handler, i))

            concurrent.futures.wait(executor_results)

        for result in executor_results:
            try:
                response = result.result()
                if isinstance(response, BaseModel):
                    yield response
                elif isinstance(response, requests.Response) and return_model:
                    response_data = (
                        response.json()[return_model._xml_root_name]
                        if hasattr(return_model, "_xml_root_name")
                        else response.json()
                    )
                    yield return_model.model_validate(response_data)
                else:
                    yield response
            except Exception as err:
                logger.warning(err)
                if return_exceptions:
                    yield err
                else:
                    continue
