Getting Started
===============

Install
-------

Install the SDK from PyPI. The example is shown with your virtual environment active.

.. code-block:: console

   (.venv) % python -m pip install jamf-pro-sdk

Install Locally
---------------

Install locally into your virtual environment. You must first clone the SDK repository. The example is shown with your virtual environment active.

.. code-block:: console

    (.venv) % python -m pip install /path/to/jamf-pro-sdk-python

When running ``pip freeze`` the SDK will appear with a filepath to the source instead of the version.

.. code-block:: console

    (.venv) % pip freeze
    ...
    jamf-pro-sdk @ file:///path/to/jamf-pro-sdk-python
    ...

Create a Client
---------------

Import the Jamf Pro client from the SDK:

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider

Create a client object passing in your Jamf Pro server name and a username and password:

.. note::

    When passing your Jamf Pro server name, do not include the scheme (``https://``) as the SDK handles this automatically for you.


    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=BasicAuthProvider("oscar", "j@mf1234!")
    ... )
    >>>

The ``BasicAuthProvider`` is a credentials provider. These objects are interfaces for authenticating for access tokens to the Jamf Pro APIs. Basic auth credentials providers use a username and password for authentication when requesting a new token.

To use an API Client for authentication (`Jamf Pro 10.49+ <https://learn.jamf.com/bundle/jamf-pro-documentation-current/page/API_Roles_and_Clients.html>`_) use :class:`~jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider`.

There are a number of built-in :doc:`/reference/credentials` available. To learn how to implement your own visit :ref:`user/advanced:Custom Credentials Providers`.

.. important::

    **Do not plaintext secrets (passwords, clients secrets, etc.) in scripts or the console.** The use of the base ``BasicAuthProvider`` class in this guide is for demonstration purposes.

On the first request made the client will retrieve and cache an access token. This token will be used for all requests up until it nears expiration. At that point the client will refresh the token. If the token has expired the client will basic auth for a new one.

You can retrieve the current token at any time:

    >>> access_token = client.get_access_token()
    >>> access_token
    AccessToken(type='user', token='eyJhbGciOiJIUzI1NiJ9...', expires=datetime.datetime(2023, 8, 21, 16, 57, 1, 113000, tzinfo=datetime.timezone.utc), scope=None)
    >>> access_token.token
    'eyJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkLWFwcCI6IkdFTkVSSUMiLCJhdXRoZW50aWNhdGlvbi10eXBlIjoiSlNTIiwiZ3JvdXBzIjpbXSwic3ViamVjdC10eXBlIjoiSlNTX1VTRVJfSUQiLCJ0b2tlbi11dWlkIjoiM2Y4YzhmY2MtN2U1Ny00Njg5LThiOTItY2UzMTIxYjVlYTY5IiwibGRhcC1zZXJ2ZXItaWQiOi0xLCJzdWIiOiIyIiwiZXhwIjoxNTk1NDIxMDAwfQ.6T9VLA0ABoFO9cqGfp3vWmqllsp3zAbtIW0-M-M41-E'
    >>>

Both the Classic and Pro APIs are exposed through two interfaces:

    >>> client.classic_api
    <jamf_pro_sdk.clients.classic_api.ClassicApi object at 0x10503d240>
    >>> client.pro_api
    <jamf_pro_sdk.clients.pro_api.ProApi object at 0x10503c9d0>
    >>>

Continue on to :doc:`/user/classic_api` or the :doc:`/user/pro_api`.

Configuring the Client
----------------------

Some aspects of the Jamf Pro client can be configured at instantiation. These include TLS verification, request timeouts, retries, and pool sizes. Below is the ``SessionConfig`` object used to customize these settings:

.. autopydantic_model:: jamf_pro_sdk.models.client.SessionConfig
    :members: false

.. note::

    The ``max_concurrency`` setting is used with the SDK's concurrency features. Those are covered in :ref:`user/advanced:Performing Concurrent Operations`.

    The Jamf Developer Guide states in scalability best practices to not exceed 5 concurrent
    connections. Read more about scalability with the Jamf Pro APIs
    `here <https://developer.jamf.com/developer-guide/docs/jamf-pro-api-scalability-best-practices>`_.

The Jamf Pro client will create a default configuration if one is not provided.

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider, SessionConfig
    >>> config = SessionConfig()
    >>> config
    SessionConfig(timeout=None, max_retries=0, max_concurrency=5, verify=True, cookie=None, ca_cert_bundle=None, scheme='https')
    >>>

Here are two examples on how to use a ``SessionConfig`` with the client to disable TLS verification and set a 30 second timeout:

    >>> config = SessionConfig()
    >>> config.verify = False
    >>> config.timeout = 30
    >>> config
    SessionConfig(timeout=30, max_retries=0, max_concurrency=5, verify=False, cookie=None, ca_cert_bundle=None, scheme='https')
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=BasicAuthProvider("oscar", "j@mf1234!")
    ...     session_config=config,
    ... )
    >>>

    >>> config = SessionConfig(**{"verify": False, "timeout": 30})
    >>> config
    SessionConfig(timeout=30, max_retries=0, max_concurrency=5, verify=False, cookie=None, ca_cert_bundle=None, scheme='https')
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=BasicAuthProvider("oscar", "j@mf1234!")
    ...     session_config=config,
    ... )
    >>>

.. warning::

    It is strongly recommended you do not disable TLS certificate verification.

Logging
-------

You can quickly setup console logging using the provided :func:`~jamf_pro_sdk.helpers.logger_quick_setup` function.

    >>> import logging
    >>> from jamf_pro_sdk.helpers import logger_quick_setup
    >>> logger_quick_setup(level=logging.DEBUG)

When set to ``DEBUG`` the stream handler and level will also be applied to ``urllib3``'s logger. All logs will appear

If you require different handlers or formatting you may configure the SDK's logger manually.

    >>> import logging
    >>> sdk_logger = logging.getLogger("jamf_pro_sdk")
