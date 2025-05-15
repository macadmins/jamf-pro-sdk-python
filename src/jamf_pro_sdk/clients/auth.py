import json
import logging
from datetime import datetime, timedelta, timezone
from getpass import getpass
from threading import Lock
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

try:
    import boto3
except ImportError:
    BOTO3_IS_INSTALLED = False
    boto3 = None
else:
    BOTO3_IS_INSTALLED = True

try:
    import keyring
except ImportError:
    KEYRING_IS_INSTALLED = False
    keyring = None
else:
    KEYRING_IS_INSTALLED = True

import requests

if TYPE_CHECKING:
    from . import JamfProClient

from ..exceptions import CredentialsError
from ..models.client import AccessToken

logger = logging.getLogger("jamf_pro_sdk")


class CredentialsProvider:
    """The base credentials provider class all other providers should inherit from."""

    def __init__(self):
        self._client: Optional["JamfProClient"] = None
        self._global_lock = Lock()
        self._access_token = AccessToken()

    def attach_client(self, client: "JamfProClient"):
        self._client = client

    def get_access_token(self, thread_lock: Lock = None) -> AccessToken:
        """Thread safe method for obtaining the current API access token.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        if not thread_lock:
            thread_lock = self._global_lock

        with thread_lock:
            self._refresh_access_token()
            return self._access_token

    def _request_access_token(self) -> AccessToken:
        """This internal method requests a new Jamf Pro access token.

        Custom credentials providers should override this method. Refer to the ``ApiClientProvider``
        and ``UserCredentialsProvider`` classes for example implementations.

        This method must always return an :class:`~jamf_pro_sdk.models.client.AccessToken` object.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        return AccessToken()

    def _keep_alive(self) -> AccessToken:
        """Refresh an access token using the ``keep-alive`` endpoint.

        As of Jamf Pro 10.49 this is only supported by user bearer tokens.

        This method may be removed in a future update.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        logger.debug("Refreshing access token with 'keep-alive'")
        try:
            with self._client.session.post(
                url=f"{self._client.base_server_url}/api/v1/auth/keep-alive",
                headers={
                    "Authorization": f"Bearer {self._access_token.token}",
                    "Accept": "application/json",
                },
                timeout=15,
            ) as resp:
                return AccessToken(type="user", **resp.json())
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            logger.debug(err.response.text)
            raise

    def _refresh_access_token(self) -> None:
        """Requests and stores an API access token.

        Refresh behavior is determined by the token's type.

        For user bearer tokens, if the cached token's remaining time is greater than or equal to 60
        seconds it will be returned. If the cached token's remaining time is greater than 5 seconds
        but less than 60 seconds the token will be refreshed using the ``keep-alive`` API.

        For OAuth tokens, if the cached token's remaining time is greater than or equal to 3 seconds
        it will be returned.

        If the above conditions are not met a new token will be requested.
        """
        if self._client is None:
            raise CredentialsError("A Jamf Pro client is not attached to this credentials provider")
        kwargs: Dict[str, Any]

        # TODO: Future OAuth flows may need to set different TTL values for refresh behavior
        token_cache_ttl = 60 if self._access_token.type == "user" else 3

        # Return the cached token if expiration is below the cache TTL
        if (
            self._access_token.token
            and not self._access_token.is_expired
            and self._access_token.seconds_remaining >= token_cache_ttl
        ):
            logger.debug(
                "Using cached access token (%ds remaining)",
                self._access_token.seconds_remaining,
            )
            self._access_token = self._access_token
        # Refresh the cached user bearer token using 'keep-alive'
        elif (
            self._access_token.token
            and self._access_token.type == "user"
            and not self._access_token.is_expired
            and 5 < self._access_token.seconds_remaining < token_cache_ttl
        ):
            self._access_token = self._keep_alive()
        # Request a new token
        else:
            self._access_token = self._request_access_token()


class ApiClientCredentialsProvider(CredentialsProvider):
    def __init__(self, client_id: str, client_secret: str):
        """A credentials provider that uses OAuth2 client credentials flow using an API client.

        :param client_id: The client ID.
        :type client_id: str

        :param client_secret: The client secret.
        :type client_secret: str
        """
        self.client_id = client_id
        self.client_secret = client_secret
        super().__init__()

    def _request_access_token(self) -> AccessToken:
        """Request a new an API access token using client credentials flow."""
        with self._client.session.post(
            url=f"{self._client.base_server_url}/api/oauth/token",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
            timeout=15,
        ) as resp:
            try:
                logger.debug(
                    "Requesting new access token (%ds remaining)",
                    self._access_token.seconds_remaining,
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logger.error(err)
                logger.debug(err.response.text)
                raise

            logger.debug(resp.content)
            resp_data = resp.json()
            return AccessToken(
                type="oauth",
                token=resp_data["access_token"],
                expires=datetime.now(timezone.utc) + timedelta(seconds=resp_data["expires_in"]),
                scope=resp_data["scope"].split(),
            )


class UserCredentialsProvider(CredentialsProvider):
    def __init__(self, username: str, password: str):
        """Credentials provider that uses a username and password for obtaining access
        tokens.

        :param username: The Jamf Pro API username.
        :type username: str

        :param password: The Jamf Pro API password.
        :type password: str
        """
        self.username = username
        self.password = password
        super().__init__()

    def _request_access_token(self) -> AccessToken:
        """Request a new an API access token using user authentication."""
        with self._client.session.post(
            url=f"{self._client.base_server_url}/api/v1/auth/token",
            auth=(self.username, self.password),
            headers={"Accept": "application/json"},
            timeout=15,
        ) as resp:
            try:
                logger.debug(
                    "Requesting new access token (%ds remaining)",
                    self._access_token.seconds_remaining,
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logger.error(err)
                logger.debug(err.response.text)
                raise

            return AccessToken(type="user", **resp.json())


def prompt_for_credentials(provider_type: Type[CredentialsProvider]) -> CredentialsProvider:
    """Prompts the user for credentials based on the given provider type.

    Supports both user credentials (username/password) and API client credentials
    (client_id/client_secret), prompting interactively as needed.

    :param provider_type: The credentials provider class to instantiate.
    :type provider_type: Type[CredentialsProvider]
    :return: The ``CredentialsProvider`` object.
    :rtype: CredentialsProvider
    """
    if issubclass(provider_type, UserCredentialsProvider):
        username = input("Jamf Pro Username: ")
        password = getpass("Jamf Pro Password: ")
        return provider_type(username, password)
    elif issubclass(provider_type, ApiClientCredentialsProvider):
        client_id = input("API Client ID: ")
        client_secret = getpass("API Client Secret: ")
        return provider_type(client_id, client_secret)
    else:
        raise TypeError(f"Unsupported credentials provider: {provider_type}")


def load_from_aws_secrets_manager(
    provider_type: Type[CredentialsProvider],
    secret_id: str,
    version_id: str = None,
    version_stage: str = None,
) -> CredentialsProvider:
    """A basic auth credentials provider for AWS Secrets Manager.
    Requires an IAM role with the ``secretsmanager:GetSecretValue`` permission. May also require
    ``kms:Decrypt`` if the secret is encrypted with a customer managed key.

    The ``SecretString`` is expected to be JSON string in this format:

    .. code-block:: json

        // For UserCredentialsProvider:
        {
            "username": "oscar",
            "password": "*****"
        }

        // For ApiClientCredentialsProvider:
        {
            "client_id": "abc123",
            "client_secret": "xyz456"
        }

    .. important::

        This credentials provider requires the ``aws`` extra dependency.

    :param provider_type: The credentials provider class to instantiate using the loaded secret.
    :type provider_type: Type[CredentialsProvider]

    :param secret_id: The ARN or name of the secret.
    :type secret_id: str

    :param version_id: The unique identifier of this version of the secret. If not
        provided the latest version of the secret will be returned.
    :type version_id: str

    :param version_stage: The staging label of the version of the secret to retrieve.
    :type version_stage: str

    :return: The ``CredentialsProvider`` object with necessary credentials.
    :rtype: CredentialsProvider
    """
    if not BOTO3_IS_INSTALLED:
        raise ImportError("The 'aws' extra dependency is required.")

    secrets_client = boto3.client("secretsmanager")
    kwargs = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage

    secret_value = secrets_client.get_secret_value(**kwargs)
    credentials = json.loads(secret_value["SecretString"])
    return provider_type(**credentials)


def load_from_keychain(
    provider_type: Type[CredentialsProvider], server: str
) -> CredentialsProvider:
    """Load credentials from the macOS login keychain and return an instance of the
    specified credentials provider.

    The Jamf Pro API password or client credentials are stored in the keychain with
    the ``service_name`` set to the Jamf Pro server name.

    Supports:
        - ``UserCredentialsProvider``: retrieves password using provided username
        - ``ApiClientCredentialsProvider``: retrieves Client ID and Client Secret using usernames of
            "CLIENT_ID" and "CLIENT_SECRET"

    .. important::

        This credentials provider requires the ``macOS`` extra dependency.

    :param provider_type: The credentials provider class to instantiate
    :type provider_type: Type[CredentialsProvider]

    :param server: The Jamf Pro server name.
    :type server: str

    :return: An instantiated credentials provider using the keychain values.
    :rtype: CredentialsProvider
    """
    if not KEYRING_IS_INSTALLED:
        raise ImportError("The 'macOS' extra dependency is required.")

    if server.startswith("http://"):
        server = "https://" + server[len("http://") :]
    elif not server.startswith("https://"):
        server = f"https://{server}"

    if issubclass(provider_type, UserCredentialsProvider):
        username = input("Jamf Pro Username: ")
        password = keyring.get_password(service_name=server, username=username)
        if password is None:
            raise CredentialsError(
                f"Password not found for server {server} and username {username}"
            )
        return provider_type(username, password)
    elif issubclass(provider_type, ApiClientCredentialsProvider):
        client_id = keyring.get_password(service_name=server, username="CLIENT_ID")
        client_secret = keyring.get_password(service_name=server, username="CLIENT_SECRET")
        if not client_id or not client_secret:
            raise CredentialsError(
                f"API Credentials were not found for server {server}. Please verify they are in the correct format."
            )
        return provider_type(client_id, client_secret)
    else:
        raise TypeError(f"Unsupported credentials provider: {provider_type}")
