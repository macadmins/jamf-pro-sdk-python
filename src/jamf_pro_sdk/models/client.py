import platform
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from ..__about__ import __version__
from . import BaseModel

DEFAULT_USER_AGENT = f"JamfProSDK/{__version__} {platform.system()}/{platform.release()} Python/{platform.python_version()}"
EPOCH_DATETIME = datetime(1970, 1, 1, tzinfo=timezone.utc)


class Schemes(str, Enum):
    http = "http"
    https = "https"


class SessionConfig(BaseModel):
    """Jamf Pro client session configuration.

    :param timeout: HTTP request timeout (defaults to no timeout set).
    :type timeout: int

    :param max_retries: HTTP request retries (defaults to `0`).
    :type max_retries: int

    :param max_concurrency: The maximum number of HTTP connections the client will create when
        making concurrent requests (defaults to `5`).
    :type max_concurrency: int

    :param return_exceptions: Global setting that controls returning exceptions when
        :meth:`~jamf_pro_sdk.clients.JamfProClient.concurrent_operations` is invoked.  Setting this
        to ``True`` will return the exception object if an error is encountered by the ``handler``.
        If ``False`` no response will be given for that operation.

    :param user_agent: Override the default ``User-Agent`` string included with SDK requests.
    :type user_agent: str

    :param verify: TLS certificate verification (defaults to `True`).
    :type verify: bool

    :param cookie: A path to a text cookie file to attach to the client session.
    :type cookie: str | Path

    :param ca_cert_bundle: A path to a CA cert bundle to use in addition to the system trust store.
    :type ca_cert_bundle: str | Path

    :param scheme: Override the URL scheme to `http` (defaults to `https`). **It is strongly
        advised that you use HTTPS for certificate verification.**
    :type scheme: str
    """

    timeout: Optional[int] = None
    max_retries: int = 0
    max_concurrency: int = 5
    return_exceptions: bool = True
    user_agent: str = DEFAULT_USER_AGENT
    verify: bool = True
    cookie: Optional[Union[str, Path]] = None
    ca_cert_bundle: Optional[Union[str, Path]] = None
    scheme: Schemes = Schemes.https


class AccessToken(BaseModel):
    """Jamf Pro access token. Used by a :class:`~jamf_pro_sdk.clients.auth.CredentialsProvider`
    object to manage an access token.

    :param type: The type name of the access token. This should only be ``user`` or ``oauth``.
    :type type: str

    :param token: The raw access token string.
    :type token: str

    :param expires: The expiration time of the token represented as a ``datetime`` object.
    :type expires: datetime

    :param scope: If the access token is an ``oauth`` type the scope claim will be passed as a list
        of string values.
    :type scope: List[str]
    """

    type: str = ""
    token: str = ""
    expires: datetime = EPOCH_DATETIME
    scope: Optional[List[str]] = None

    def __str__(self):
        return self.token

    @property
    def is_expired(self) -> bool:
        """Has the current time passed the token's expiration time?
        Will return `False` if the current time is within 5 seconds of the
        token's expiration time.
        """
        return self.expires - timedelta(seconds=5) < datetime.now(timezone.utc)

    @property
    def seconds_remaining(self) -> int:
        """The number of seconds until the token expires."""
        return max(0, int((self.expires - datetime.now(timezone.utc)).total_seconds()))
