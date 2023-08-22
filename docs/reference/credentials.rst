:tocdepth: 3

Credentials Providers
=====================

API Client Providers
--------------------

These credentials providers use Jamf Pro API clients for API authentication.

.. autoclass:: jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider
    :members:

Basic Auth Providers
--------------------

These credentials providers use a username and password for API authentication.

.. autoclass:: jamf_pro_sdk.clients.auth.BasicAuthProvider
    :members:

.. autoclass:: jamf_pro_sdk.clients.auth.PromptForCredentials
    :members:

.. autoclass:: jamf_pro_sdk.clients.auth.LoadFromKeychain
    :members:

.. autoclass:: jamf_pro_sdk.clients.auth.LoadFromAwsSecretsManager
    :members:

Access Token
------------

.. autopydantic_model:: jamf_pro_sdk.models.client.AccessToken
    :undoc-members: false

Credentials Provider Base Class
-------------------------------

.. autoclass:: jamf_pro_sdk.clients.auth.CredentialsProvider
    :members:
    :private-members:
