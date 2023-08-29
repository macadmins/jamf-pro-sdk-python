Pro API
=======

The Pro API only returns and accepts JSON data. API responses are returned as data models that can be interacted with using dot notation.

Read Requests
-------------

Write Requests
--------------

Pagination
----------

Some Pro API read operations support pagination. The API will return a partial response if there are more results than the set page size of the request. To obtain more results the next page must be requested.

The SDK uses a ``Paginator`` to automatically handle this.

.. autoclass:: jamf_pro_sdk.clients.pro_api.Paginator
    :members:

If the total number of results in the first request are greater than the page size the paginator will fetch all of the remaining pages concurrently.

.. tip::

    If you have large number of records in a paginated request, you may find that using a smaller page size is *faster* than setting a larger (or max) page size.

Paginators can either return the full response of all pages at once, or it can return a generator to iterate over the pages. This can be useful if results may contain hundreds or thousands of items that you do not want to keep in memory as you are processing them.

The curated methods will return all results by default. Each operation that supports pagination allows this behavior to be overridden to return the generator.

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider
    >>> client = JamfProClient("dummy.jamfcloud.com", BasicAuthProvider("demo", "tryitout"))
    >>> response = client.pro_api.get_computer_inventory_v1(return_generator=True)
    >>> response
    <generator object Paginator._request at 0x105290120>

The paginator object itself will return the generator by default. This can be overridden in much the same way.

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider
    >>> from jamf_pro_sdk.clients.pro_api.pagination import Paginator
    >>> from jamf_pro_sdk.models.pro.computers import Computer
    >>> client = JamfProClient("dummy.jamfcloud.com", BasicAuthProvider("demo", "tryitout"))
    >>> paginator = Paginator(api_client=client.pro_api, resource_path="v1/computers-inventory", return_model=Computer)
    >>> paginator()
    <generator object Paginator._request at 0x1052c2dd0>
    >>> paginator(return_generator=False)
    [Computer(id='117', udid='a311b7c8-75ee-48cf-9b1b-a8598f013366', general=ComputerGeneral(name='Backancient',...

Many paginated API read operations also support query parameters to filter and sort the results so you can reduce the number of items returned in a request.

The SDK provides programmatic interfaces for both of these options that will properly construct the expressions.

.. _Pro API Filtering:

Filtering
---------

A filter expression is returned from a ``FilterField`` object when one of the operators is called.

The example below creates a filter expression requiring the ID of every result must be equal to ``1``.

.. code-block:: python

    >>> from jamf_pro_sdk.clients.pro_api.pagination import FilterField
    >>> filter_expression = FilterField("id").eq(1)
    >>> print(filter_expression)
    id==1
    >>>

Filters can be combined together using Python's ``&`` and ``|`` binary operands.

The example below creates a filter expression requiring the ID of every result is below ``100`` and the value of the asset tag is below ``1000``.

.. code-block:: python

    >>> from jamf_pro_sdk.clients.pro_api.pagination import FilterField
    >>> filter_expression = FilterField("id").gt(100) & FilterField("general.assetTag").lt(1000)
    >>> print(filter_expression)
    id>100;general.assetTag<1000
    >>>

``AND`` operators take precedence and are evaluated before any ``OR`` operators. Filters can be grouped together and the result of the inner filters will be evaluated in order with the outer filters.

The example below creates a filter expression requiring either the barcode or the asset tag of every result to be below ``1000`` and the ID be below ``100``.

.. code-block:: python

    >>> from jamf_pro_sdk.clients.pro_api.pagination import FilterField, filter_group
    >>> filter_expression = filter_group(FilterField("general.barcode1").lt(1000) | FilterField("general.assetTag").lt(1000)) & FilterField("id").gte(100)
    >>> print(filter_expression)
    (general.barcode1<1000,general.assetTag<1000);id>=100
    >>>

.. _Pro API Sorting:

Sorting
-------

Sorting expressions work similarly. A sort expression is returned from a ``SortField`` object when one of the operators is called.

.. code-block:: python

    >>> from jamf_pro_sdk.clients.pro_api.pagination import SortField
    >>> sort_expression = SortField("id").asc()
    >>> print(sort_expression)
    id:asc
    >>>

Sortable fields can be combined together using Python's ``&`` binary operands. Unlike filter, sort fields are evaluated from left-to-right. The leftmost field will be the first sort, and then the next, and so on.

.. code-block:: python

    >>> from jamf_pro_sdk.clients.pro_api.pagination import SortField
    >>> sort_expression = SortField("name").asc() & SortField("id").desc()
    >>> print(sort_expression)
    name:asc,id:desc
    >>>
