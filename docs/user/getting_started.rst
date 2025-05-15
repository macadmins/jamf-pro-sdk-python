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

Create a client object using an API Client ID and Client Secret - the **recommended** method for authentication:

.. important::

    **Breaking Change**: As of version ``0.8a1``, the SDK no longer uses ``BasicAuthProvider`` objects. Use :class:`~jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider` as the new default.

    `Basic authentication is now disabled by default  <https://developer.jamf.com/jamf-pro/docs/classic-api-authentication-changes#basic-authentication>`_ in Jamf Pro. To authenticate securely and ensure compatibility with future Jamf Pro versions, use an API Client for access tokens instead.

.. code-block:: python
    
    >>> from jamf_pro_sdk import JamfProClient, ApiClientCredentialsProvider
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=ApiClientCredentialsProvider("client_id", "client_secret")
    ... )
    >>>

.. _server_scheme:

.. note::

    When passing your Jamf Pro server name, do not include the scheme (``https://``) as the SDK handles this automatically for you.

Choosing a Credential Provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are a number of built-in :doc:`/reference/credentials` available. To learn how to implement your own visit :ref:`user/advanced:Custom Credentials Providers`.

**We recommend using API Clients** for most cases. Basic authentication via username and password is now considered a legacy method and is **disabled by default** in Jamf Pro versions ≥ 10.49. 

- Use :class:`~jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider` for API Clients. 
- Use :class:`~jamf_pro_sdk.clients.auth.UserCredentialsProvider` if enabled in your Jamf environment. 

.. important::

    **Do not use plaintext secrets (passwords, clients secrets, etc.) in scripts or the console.** The use of the base ``UserCredentialsProvider`` class in this guide is for demonstration purposes.

Credential Provider Utility Functions
-------------------------------------

The SDK contains three helper functions that will *return* an instantiated credential provider of the specified type. When leveraging these functions, ensure you have the required extra dependencies installed. 

Prompting for Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, ApiClientCredentialsProvider, prompt_for_credentials
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=prompt_for_credentials(
    ...         provider_type=ApiClientCredentialsProvider
    ...     )
    ... )
    API Client ID: 123456abcdef 
    API Client Secret:   

Loading from AWS Secrets Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important:: 

    The ``aws`` dependency is required for this function and can be installed with ``% python3 -m pip install 'jamf-pro-sdk[aws]'``.

The ``SecretString`` is expected to be a JSON string in the following format:

.. code-block:: json

    // For UserCredentialsProvider:
    {
        "username": "oscar",
        "password": "******"
    }

    // For ApiClientCredentialsProvider:
    {
        "client_id": "abc123",
        "client_secret": "xyz456"
    }

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, ApiClientCredentialsProvider, load_from_aws_secrets_manager
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=load_from_aws_secrets_manager(
    ...         provider_type=ApiClientCredentialsProvider,
    ...         secret_id="arn:aws:secretsmanager:us-west-2:111122223333:secret:aes128-1a2b3c"    
    ...     )
    ... )   

Loading from Keychain
^^^^^^^^^^^^^^^^^^^^^

.. important::

    This utility requires the ``keyring`` extra dependency, which can be installed via ``% python3 -m pip install 'jamf-pro-sdk[macOS]'``. 

    When using :class:`~jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider`, the SDK expects the client ID and client secret to be stored using the format ``CLIENT_ID`` and ``CLIENT_SECRET`` respectively. For :class:`~jamf_pro_sdk.clients.auth.UserCredentialsProvider`, you will be prompted for a username. 
    
    Additionally, the :ref:`server scheme <server_scheme>` does not need to be passed to the ``server`` argument, as the SDK handles this for you.

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, ApiClientCredentialsProvider, load_from_keychain
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=load_from_keychain(
    ...         provider_type=ApiClientCredentialsProvider,
    ...         server="jamf.my.org"    
    ...     )    
    ... )

Access Tokens
-------------

On the first request made the client will retrieve and cache an access token. This token will be used for all requests up until it nears expiration. At that point the client will refresh the token. If the token has expired, the client will use the configured credentials provider to request a new one.

You can retrieve the current token at any time:

.. code-block:: python

    >>> access_token = client.get_access_token()
    >>> access_token
    AccessToken(type='user', token='eyJhbGciOiJIUzI1NiJ9...', expires=datetime.datetime(2023, 8, 21, 16, 57, 1, 113000, tzinfo=datetime.timezone.utc), scope=None)
    >>> access_token.token
    'eyJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkLWFwcCI6IkdFTkVSSUMiLCJhdXRoZW50aWNhdGlvbi10eXBlIjoiSlNTIiwiZ3JvdXBzIjpbXSwic3ViamVjdC10eXBlIjoiSlNTX1VTRVJfSUQiLCJ0b2tlbi11dWlkIjoiM2Y4YzhmY2MtN2U1Ny00Njg5LThiOTItY2UzMTIxYjVlYTY5IiwibGRhcC1zZXJ2ZXItaWQiOi0xLCJzdWIiOiIyIiwiZXhwIjoxNTk1NDIxMDAwfQ.6T9VLA0ABoFO9cqGfp3vWmqllsp3zAbtIW0-M-M41-E'
    >>>

Both the Classic and Pro APIs are exposed through two interfaces:

.. code-block:: python

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

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, ApiClientCredentialsProvider, SessionConfig
    >>> config = SessionConfig()
    >>> config
    SessionConfig(timeout=None, max_retries=0, max_concurrency=5, verify=True, cookie=None, ca_cert_bundle=None, scheme='https')
    >>>

Here are two examples on how to use a ``SessionConfig`` with the client to disable TLS verification and set a 30 second timeout:

.. code-block:: python

    >>> config = SessionConfig()
    >>> config.verify = False
    >>> config.timeout = 30
    >>> config
    SessionConfig(timeout=30, max_retries=0, max_concurrency=5, verify=False, cookie=None, ca_cert_bundle=None, scheme='https')
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=ApiClientCredentialsProvider("client_id", "client_secret"),
    ...     session_config=config,
    ... )
    >>>

    >>> config = SessionConfig(**{"verify": False, "timeout": 30})
    >>> config
    SessionConfig(timeout=30, max_retries=0, max_concurrency=5, verify=False, cookie=None, ca_cert_bundle=None, scheme='https')
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=ApiClientCredentialsProvider("client_id", "client_secret"),
    ...     session_config=config,
    ... )
    >>>

.. warning::

    It is strongly recommended you do not disable TLS certificate verification.

Logging
-------

You can quickly setup console logging using the provided :func:`~jamf_pro_sdk.helpers.logger_quick_setup` function.

.. code-block:: python
    
    >>> import logging
    >>> from jamf_pro_sdk.helpers import logger_quick_setup
    >>> logger_quick_setup(level=logging.DEBUG)

When set to ``DEBUG`` the stream handler and level will also be applied to ``urllib3``'s logger. All logs will appear

If you require different handlers or formatting you may configure the SDK's logger manually.

.. code-block:: python
    
    >>> import logging
    >>> sdk_logger = logging.getLogger("jamf_pro_sdk")
