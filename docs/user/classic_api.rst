Classic API
===========

The Classic API only accepts XML for write operations, but allows JSON for read operations. The Classic API interface for the SDK only accepts JSON data in read responses. API responses are returned as data models that can be more easily interacted with using dot notation.

Read Requests
-------------

The curated methods return data models of the JSON response. Data models can be interacted with using dot notation.

.. code-block:: python

    >>> computers = client.classic_api.list_all_computers()
    >>> len(computers)
    4
    >>> type(computers[0])
    <class 'jamf_pro_sdk.models.classic.computers.ComputersItem'>
    >>> for c in computers:
    ...   print(c.name)
    ...
    Oscar's MacBook Air
    Chip's MacBook Pro
    Zach's MacBook Air
    Bryson’s MacBook Pro
    >>>

Some Classic API operations support ``subsets`` which extend or limit the data that is returned:

.. code-block:: python

    >>> computers = client.classic_api.list_all_computers(subsets=["basic"])
    >>> computers[0]
    ComputersItem(id=1, name="Oscar's MacBook Air", managed=True, username='oscar', model='MacBookPro18,3', department='', building='', mac_address='00:1A:2B:CD:34:FF', udid='2AD4F6B0-3926-4305-B567-C1FB93F36768', serial_number='TGIF772PLY', report_date_utc=datetime.datetime(2022, 12, 16, 22, 38, 51, 347000, tzinfo=datetime.timezone.utc), report_date_epoch=1671230331347)
    >>>

ISO 8601 date fields (generally, fields that end with `_date_utc`) are automatically converted into ``datetime.datetime`` objects:

.. code-block:: python

    >>> computers[0].report_date_utc
    datetime.datetime(2022, 12, 16, 22, 38, 51, 347000, tzinfo=datetime.timezone.utc)
    >>>

The data models can also be converted back into a Python ``dict``:

.. code-block:: python

    >>> computers[0].dict()
    {'id': 1, 'name': "Oscar's MacBook Pro", 'managed': True, 'username': 'oscar', 'model': 'MacBookPro18,3', 'department': '', 'building': '', 'mac_address': '00:1A:2B:CD:34:FF"', 'udid': '2AD4F6B0-3926-4305-B567-C1FB93F36768', 'serial_number': 'TGIF772PLY', 'report_date_utc': datetime.datetime(2022, 12, 16, 22, 38, 51, 347000, tzinfo=datetime.timezone.utc), 'report_date_epoch': 1671230331347}
    >>>

.. tip::

    You can browse the available data models at :doc:`/reference/models_classic`.

Write Requests
--------------

The Classic API only accepts XML for ``POST`` and ``PUT`` operations. The SDK accepts XML strings if you are generating this data, or you can leverage the data models and their built-in XML generation to do the work for you.

Here is an example where an extension attribute value is being updated:

.. code-block:: python

    >>> from jamf_pro_sdk.models.classic.computers import ClassicComputer, ClassicComputerExtensionAttribute
    >>> computer_update = ClassicComputer()
    >>> computer_update.extension_attributes.append(ClassicComputerExtensionAttribute(id=1, value="new"))
    >>> computer_update.xml()
    '<?xml version="1.0" encoding="UTF-8" ?><computer><extension_attributes><extension_attribute><id>1</id><value>new</value></extension_attribute></extension_attributes></computer>'
    >>>

You can also construct the update as a ``dict`` and pass that into the model:

.. code-block:: python

    >>> data  = {"extension_attributes": [{"id": 1, "value": "new"}]}
    >>> computer_update = ClassicComputer(**data)
    >>> computer_update.xml()
    '<?xml version="1.0" encoding="UTF-8" ?><computer><extension_attributes><extension_attribute><id>1</id><value>new</value></extension_attribute></extension_attributes></computer>'
    >>>

The SDK's data models perform type checking and some validation. By using the data models you can prevent invalid data from being set.

.. code-block:: python

    >>> bad_data = {"extension_attributes": {"id": 1, "value": "new"}}
    >>> ClassicComputer(**bad_data)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/jamf-pro-sdk/jamf_pro_sdk/models/__init__.py", line 10, in __init__
        super(BaseModel, self).__init__(*args, **kwargs)
      File "pydantic/main.py", line 342, in pydantic.main.BaseModel.__init__
    pydantic.error_wrappers.ValidationError: 1 validation error for ClassicComputer
    extension_attributes
      value is not a valid list (type=type_error.list)
    >>>

The XML string or SDK data model are passed to the ``data`` argument for write operations.
The SDK handles converting data models to XML.

.. code-block:: python

    >>> xml = '<?xml version="1.0" encoding="UTF-8" ?><computer><extension_attributes><extension_attribute><id>1</id><value>new</value></extension_attribute></extension_attributes></computer>'
    >>> client.classic_api.update_computer_by_id(computer_id=1, data=xml)

    >>> data  = {"extension_attributes": [{"id": 1, "value": "new"}]}
    >>> computer_update = ClassicComputer(**data)
    >>> client.classic_api.update_computer_by_id(computer_id=1, data=computer_update)

Example Usage
-------------

Assume this client has been instantiated for the examples shown below.

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider
    >>> client = JamfProClient(
    ...     server="jamf.my.org",
    ...     credentials=BasicAuthProvider("oscar", "j@mf1234!")
    ... )
    >>>


Update a Computer's Location
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can selectively update fields on a computer record by creating a ``ClassicComputer`` object and setting the desired fields, passing a dictionary with a model, or a raw XML string.

Using the model:

.. code-block:: python

    >>> from jamf_pro_sdk.models.classic.computers import ClassicComputer
    >>> computer_update = ClassicComputer()
    >>> computer_update.location.username = "amy"
    >>> computer_update.location.real_name = "Amy"
    >>> computer_update.location.email_address = "amy@my.org"
    >>> computer_update.xml()
    '<?xml version="1.0" encoding="UTF-8" ?><computer><location><username>amy</username><real_name>Amy</real_name><email_address>amy@my.org</email_address></location></computer>'
    >>> client.classic_api.update_computer_by_id(5, computer_update)
    >>>

Using a dictionary:

.. code-block:: python

    >>> dict_update = {'username': 'amy', 'real_name': 'Amy', 'email_address': 'amy@my.org'}
    >>> client.classic_api.update_computer_by_id(5, ClassicComputer(**dict_update))
    >>>

Using a raw XML string:

.. code-block:: python

    >>> xml_update = """<computer>
    ...     <location>
    ...         <username>amy</username>
    ...         <real_name>Amy</real_name>
    ...         <email_address>amy@my.org</email_address>
    ...     </location>
    ... </computer>"""
    >>> client.classic_api.update_computer_by_id(5, xml_update)
    >>>


Update a Static Computer Group's Membership
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Static group memberships are modified by providing an iterable of either device IDs (integers) or ``ClassicComputerGroupMember`` objects. Passing in the objects is a handy shortcut when iterating over membership results and selecting devices to add/remove from the same group or another.

.. code-block:: python

    >>> client.classic_api.get_computer_group_by_id(3)
    ClassicComputerGroup(id=3, name='Test Group 1', is_smart=False, site=Site(id=-1, name='None'), criteria=[], computers=[])
    >>>

Passing an array with an ID:

.. code-block:: python

    >>> client.classic_api.update_static_computer_group_membership_by_id(3, computers_to_add=[10])
    >>> client.classic_api.get_computer_group_by_id(3)).computers
    [ClassicComputerGroupMember(id=10, name='YohnkBook', mac_address='25:3f:d9:ec:d5:b6', alt_mac_address='77:81:eb:54:b2:6a', serial_number='CJYQC70IW2T3')]

Passing a ``ComputerGroupMember`` object:

.. code-block:: python

    >>> from jamf_pro_sdk.models.classic.computer_groups import ClassicComputerGroupMember
    >>> new_member = ClassicComputerGroupMember(id=10)
    >>> client.classic_api.update_static_computer_group_membership_by_id(3, computers_to_add=[new_member])
    >>> client.classic_api.get_computer_group_by_id(3)).computers
    [ClassicComputerGroupMember(id=10, name='YohnkBook', mac_address='25:3f:d9:ec:d5:b6', alt_mac_address='77:81:eb:54:b2:6a', serial_number='CJYQC70IW2T3')]
