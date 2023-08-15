import json
import logging
from getpass import getpass
from threading import Lock
from typing import TYPE_CHECKING, Any, Dict, Optional

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
        self._access_token = AccessToken()
        self._global_lock = Lock()

    def attach_client(self, client: "JamfProClient"):
        self._client = client

    def get_access_token(self, thread_lock: Lock = None) -> str:
        """Thread safe method for obtaining the current API access token."""
        if not thread_lock:
            thread_lock = self._global_lock

        with thread_lock:
            self._refresh_access_token()
            return self._access_token.token

    def _refresh_access_token(self) -> AccessToken:
        """This internal method creates/refreshes a Jamf Pro access token.

        Credentials providers should override this method. The ``BasicAuthProvider`` can act as a
        template for how to do this. While it caches a single access token for the client, consider
        use cases where the token is stored remotely in a cache or database.

        This method must always return an :class:`~jamf_pro_sdk.clients.auth.AccessToken` object.

        :return: An ``AccessToken`` object.
        :rtype: AccessToken
        """
        return AccessToken()


class ApiClientProvider(CredentialsProvider):
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


class BasicAuthProvider(CredentialsProvider):
    def __init__(self, username: str, password: str):
        """A credentials provider that uses a username and password for obtaining access tokens.

        :param username: The Jamf Pro API username.
        :type username: str

        :param password: The Jamf Pro API password.
        :type password: str
        """
        self.username = username
        self.password = password
        super().__init__()

    def _refresh_access_token(self) -> AccessToken:
        """Returns or obtains an API access token.

        Jamf Pro access tokens have a default  expiration of 30 minutes.

        If the cached token's remaining time is greater than or equal to 60 seconds it
        will be returned.

        If the cached token's remaining time is greater than 5 seconds but less than 60
        seconds a new token will be created using the ``keep-alive`` API.

        If the above conditions are not met a new token will be created using the original
        username and password in the credentials object.
        """
        if self._client is None:
            raise CredentialsError("A Jamf Pro client is not attached to this credentials provider")
        kwargs: Dict[str, Any]

        if (
            self._access_token.token
            and not self._access_token.is_expired
            and self._access_token.seconds_remaining >= 60
        ):
            # The cached token does not need to be refreshed
            logger.debug(
                "Using cached access token (%ds remaining)",
                self._access_token.seconds_remaining,
            )
            return self._access_token
        if (
            self._access_token.token
            and not self._access_token.is_expired
            and 5 < self._access_token.seconds_remaining < 60
        ):
            # Refresh the cached token if its expiration is 5-59 seconds
            kwargs = {
                "url": f"{self._client.base_server_url}/api/v1/auth/keep-alive",
                "headers": {
                    "Authorization": f"Bearer {self._access_token.token}",
                    "Accept": "application/json",
                },
            }
        else:
            # Basic auth must be used to obtain a new token.
            # A default timeout of 5 seconds is enforced.
            kwargs = {
                "url": f"{self._client.base_server_url}/api/v1/auth/token",
                "auth": (self.username, self.password),
                "headers": {"Accept": "application/json"},
                "timeout": 5,
            }

        with self._client.session.post(**kwargs) as resp:
            try:
                logger.debug(
                    "Requesting new access token %s (%ds remaining)",
                    kwargs["url"],
                    self._access_token.seconds_remaining,
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logger.error(err)
                logger.debug(err.response.text)
                raise

        self._access_token = AccessToken(**resp.json())


class PromptForCredentials(BasicAuthProvider):
    def __init__(self, username: Optional[str] = None):
        """A credentials provider for command-line uses cases. The user will be prompted for their
        username (if not provided) and password.

        :param username: The Jamf Pro API username.
        :type username: Optional[str]
        """
        if username is None:
            username = input("Jamf Pro Username: ")
        password = getpass("Jamf Pro Password: ")
        super().__init__(username, password)


class LoadFromAwsSecretsManager(BasicAuthProvider):
    def __init__(self, secret_id: str, version_id: str = None, version_stage: str = None):
        """A credentials provider for AWS Secrets Manager.
        Requires ``secretsmanager:GetSecretValue`` permission. May also require
        ``kms:Decrypt`` if the secret is encrypted with a customer managed key.

        The ``SecretString`` is expected to be JSON string in this format:

        .. code-block:: json

            {
                "username": "oscar",
                "password": "*****"
            }

        :param secret_id: The ARN or name of the secret.
        :type secret_id: str

        :param version_id: The unique identifier of this version of the secret. If not
            provided the latest version of the secret will be returned.
        :type version_id: str

        :param version_stage: The staging label of the version of the secret to retrieve.
        :type version_stage: str
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
        username = credentials["username"]
        password = credentials["password"]

        super().__init__(username, password)


class LoadFromKeychain(BasicAuthProvider):
    def __init__(self, server: str, username: str):
        """A credentials provider for the macOS login keychain. The API password is stored in a
        keychain entry where the ``service_name`` is the server.

        :param server: The Jamf Pro server name.
        :type server: str

        :param username: The Jamf Pro API username.
        :type username: str
        """
        if not KEYRING_IS_INSTALLED:
            raise ImportError("The 'macOS' extra dependency is required.")

        username = username
        password = keyring.get_password(service_name=server, username=username)

        if password is None:
            raise CredentialsError(
                f"Password not found for server {server} and username {username}"
            )

        super().__init__(username, password)
