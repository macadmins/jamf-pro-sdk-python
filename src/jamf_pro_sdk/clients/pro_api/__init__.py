from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, List, Union

from ...models.pro.computers import Computer
from ...models.pro.jcds2 import DownloadUrl, File, NewFile
from .api_options import *
from .pagination import Paginator

if TYPE_CHECKING:
    import requests

    from .pagination import FilterExpression, Page, SortExpression


class ProApi:
    """Provides an interface to the Jamf Pro API."""

    def __init__(
        self,
        request_method: Callable[..., requests.Response],
        concurrent_requests_method: Callable[..., Iterator],
    ):
        self.api_request = request_method
        self.concurrent_api_requests = concurrent_requests_method

    # Computer Inventory APIs

    def get_computer_inventory_v1(
        self,
        sections: List[str] = None,
        start_page: int = 0,
        page_size: int = 100,
        sort_expression: SortExpression = None,
        filter_expression: FilterExpression = None,
        return_generator: bool = False,
    ) -> Union[List[Computer], Iterator[Page]]:
        """Returns a list of computer inventory records.

        :param sections: (optional) Select which sections of the computer's details to return. If
            not specific the request will default to ``GENERAL``. If ``ALL`` is passed then all
            sections will be returned.

            Allowed sections:

            .. autoapioptions:: jamf_pro_sdk.clients.pro_api.api_options.get_computer_inventory_v1_allowed_sections

        :type sections: List[str]

        :param start_page: (optional) The page to begin returning results from. See
            :class:`Paginator` for more information.
        :type start_page: int

        :param page_size: (optional) The number of results to include in each requested page. See
            :class:`Paginator` for more information.
        :type page_size: int

        :param sort_expression: (optional) The sort fields to apply to the request. See the
            documentation for :ref:`Pro API Sorting` for more information.

            Allowed sort fields:

            .. autoapioptions:: jamf_pro_sdk.clients.pro_api.api_options.get_computer_inventory_v1_allowed_sort_fields

        :type sort_expression: SortExpression

        :param filter_expression: (optional) The filter expression to apply to the request. See the
            documentation for :ref:`Pro API Filtering` for more information.

            Allowed filter fields:

            .. autoapioptions:: jamf_pro_sdk.clients.pro_api.api_options.get_computer_inventory_v1_allowed_filter_fields

        :type filter_expression: FilterExpression

        :param return_generator: If ``True`` a generator is returned to iterate over pages. By
            default, the results for all pages will be returned in a single response.
        :type return_generator: bool

        :return: List of computers OR a paginator generator.
        :rtype: List[~jamf_pro_sdk.models.pro.computer.Computer] | Iterator[Page]

        """
        if not sections:
            sections = ["GENERAL"]
        elif "ALL" in sections:
            sections = get_computer_inventory_v1_allowed_sections[1:]

        if not all([i in get_computer_inventory_v1_allowed_sections for i in sections]):
            raise ValueError(
                f"Values for 'sections' must be one of: {', '.join(get_computer_inventory_v1_allowed_sections)}"
            )

        if sort_expression:
            sort_expression.validate(get_computer_inventory_v1_allowed_sort_fields)

        if filter_expression:
            filter_expression.validate(get_computer_inventory_v1_allowed_filter_fields)

        paginator = Paginator(
            api_client=self,
            resource_path="v1/computers-inventory",
            return_model=Computer,
            start_page=start_page,
            page_size=page_size,
            sort_expression=sort_expression,
            filter_expression=filter_expression,
            extra_params={"section": ",".join(sections)},
        )

        return paginator(return_generator=return_generator)

    # JCDS APIs

    def get_jcds_files_v1(self) -> List[File]:
        """Return a list of files in the JCDS.

        :return: List JCDS File objects.
        :rtype: List[File]

        """
        resp = self.api_request(method="get", resource_path="v1/jcds/files")
        return [File(**i) for i in resp.json()]

    def create_jcds_file_v1(self) -> NewFile:
        """Create a new file in the JCDS.

        :return: A JCDS NewFile object.
        :rtype: NewFile

        """
        resp = self.api_request(method="post", resource_path="v1/jcds/files")
        return NewFile(**resp.json())

    def get_jcds_file_v1(self, file_name: str) -> DownloadUrl:
        """Read a JCDS file record by its filename.

        :return: A JCDS DownloadUrl object.
        :rtype: DownloadUrl

        """
        resp = self.api_request(method="get", resource_path=f"v1/jcds/files/{file_name}")
        return DownloadUrl(**resp.json())

    def delete_jcds_file_v1(self, file_name: str) -> None:
        """Delete a file from the JCDS.

        .. warning::

            This operation *WILL NOT* delete an associated package object. It is recommended to use
            :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.delete_package_by_id`.

        """
        self.api_request(method="delete", resource_path=f"v1/jcds/files/{file_name}")
