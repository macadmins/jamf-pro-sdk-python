Advanced Usage
==============

Custom Credentials Providers
----------------------------

A :class:`~jamf_pro_sdk.clients.auth.CredentialsProvider` is an interface for the SDK to obtain access tokens. The SDK comes with a number of built-in options that are detailed in the :doc:`/reference/credentials` reference. You can create your own provider by inheriting from the ``CredentialsProvider`` base class and overriding the ``_refresh_access_token`` method.

The following example does not accept a username or password and retrieves a token from a DynamoDB table in an AWS account (it is assumed an external process is managing this table entry).

    >>> import boto3
    >>> from jamf_pro_sdk.clients.auth import CredentialsProvider
    >>> from jamf_pro_sdk.models.client import AccessToken
    >>>
    >>> class DynamoDBProvider(CredentialsProvider):
    ...     def __init__(self, table_name: str):
    ...         self.table = boto3.resource("dynamodb").Table(table_name)
    ...         super().__init__()
    ...     @property
    ...     def _request_access_token(self) -> AccessToken:
    ...         item = table.get_item(Key={"pk": "access-token"})["Item"]
    ...         return AccessToken(type="user", token=item["token"], expires=item["expires"])
    ...
    >>> creds = DynamoDBProvider("my-table")
    >>> creds.get_access_token()
    AccessToken(type='user', token='eyJhbGciOiJIUzI1NiJ9...' ...)
    >>>

The built-in providers retrieve and store the username and password values on initialization, but by leveraging the override method shown above you can write providers that read/cache from remote locations on each invoke.

Using Unsupported APIs
----------------------

The SDK's clients provide curated methods to a large number of Jamf Pro APIs. Not all APIs may be implemented, and newer APIs may not be accounted for. You can still leverage the client to request any API without using the curated methods while still taking advantage of the client's session features and token management.

Here is the built-in method for getting a computer from the Classic API:

    >>> computer = client.classic_api.get_computer_by_id(1)
    >>> type(computer)
    <class 'jamf_pro_sdk.models.classic.computers.Computer'>
    >>>

The same operation can be performed by using the :meth:`~jamf_pro_sdk.clients.JamfProClient.classic_api_request` method directly:

    >>> response = client.classic_api_request(method='get', resource_path='computers/id/1')
    >>> type(response)
    <class 'requests.models.Response'>

This returns the ``requests.Response`` object unaltered. Note that in the ``resource_path`` argument you do not need to provide `JSSResource`.

Performing Concurrent Operations
--------------------------------

The SDK supports multi-threaded use. The cached access token utilizes a thread lock to prevent multiple threads from refreshing the token if it is expiring. The Jamf Pro client contains a helper method for performing concurrent operations.

Consider the need to perform a mass read operation on computer records. Serially this could take hours for Jamf Pro users with thousands or tens of thousands of devices. With even a concurrency of two the amount of time required can be cut nearly in half.

Here is a code example using :meth:`~jamf_pro_sdk.clients.JamfProClient.concurrent_api_requests` to perform a mass :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_computer_by_id` operation:

.. code-block:: python

    from jamf_pro_sdk import JamfProClient, BasicAuthProvider

    # The default concurrency setting is 10.
    client = JamfProClient(
        server="jamf.my.org",
        credentials=BasicAuthProvider("oscar", "j@mf1234!")
    )

    # Get a list of all computers, and then their IDs.
    all_computers = client.classic_api.list_all_computers()
    all_computer_ids = [c.id for c in all_computers]

    # Pass the API operation and list of IDs into the `concurrent_api_requests()` method.
    results = client.concurrent_api_requests(
        handler=client.classic_api.get_computer_by_id,
        arguments=all_computer_ids
    )

    # Iterate over the results.
    for r in results:
        print(r.general.id, r.general.name, r.location.username)

The ``handler`` is any callable function.

The ``arguments`` can be any iterable. Each item within the iterable is passed to the handler as its argument. If your handler takes multiple arguments you can use a ``dict`` which will be unpacked automatically.

Here is the functional code as above but using the ```~jamf_pro_sdk.clients.JamfProClient.classic_api_request`` method:

.. code-block:: python

    # Construct the arguments by iterating over the computer IDs and creating the argument dictionary
    results = client.concurrent_api_requests(
        handler=client.classic_api_request,
        arguments=[{"method": "get", "resource_path": f"computers/id/{i.id}"} for i in all_computer_ids],
        return_model=Computer
    )

    # Iterate over the results.
    for r in results:
        print(r.general.id, r.general.name, r.location.username)

If you have to perform more complex logic in the threaded operations you can wrap it into another function and pass that. Here is an example that is performing a read following by a conditional update.

.. code-block:: python

    def wrapper(computer_id, new_building):
        current = client.get_computer_by_id(computer_id, subsets=["location"])
        update = Computer()
        if current.location.building in ("Day 1", "Low Flying Hawk"):
            update.location.building = new_building
        else:
            return "Not Updated"

        client.update_computer_by_id(computer_id, )
        return "Updated"

    results = client.concurrent_api_requests(
        wrapper, [{"computer_id": 1, "new_building": ""}]
    )
