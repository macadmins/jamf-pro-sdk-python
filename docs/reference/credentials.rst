:tocdepth: 3

Credentials Providers
=====================

The Jamf Pro SDK has two primary types of credential providers: **API Client Credentials** and **User Credentials**.

API Client Credentials Provider
-------------------------------

Use Jamf Pro `API clients <https://developer.jamf.com/jamf-pro/docs/client-credentials>`_ for API authentication.

.. autoclass:: jamf_pro_sdk.clients.auth.ApiClientCredentialsProvider
    :members:

User Credentials Provider
-------------------------

User credential providers use a username and password for API authentication. 

.. autoclass:: jamf_pro_sdk.clients.auth.UserCredentialsProvider
    :members:

Utilities for Credential Providers
----------------------------------

These functions return an instantiated credentials provider of the specified type.

Prompt for Credentials
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: jamf_pro_sdk.clients.auth.prompt_for_credentials

Load from AWS Secrets Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: jamf_pro_sdk.clients.auth.load_from_aws_secrets_manager

Load from Keychain
^^^^^^^^^^^^^^^^^^

.. autofunction:: jamf_pro_sdk.clients.auth.load_from_keychain

Access Token
------------

.. autopydantic_model:: jamf_pro_sdk.models.client.AccessToken
    :undoc-members: false

Credentials Provider Base Class
-------------------------------

.. autoclass:: jamf_pro_sdk.clients.auth.CredentialsProvider
    :members:
    :private-members:
