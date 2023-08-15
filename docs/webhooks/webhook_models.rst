Webhook Event Validation
========================

The Jamf Pro SDK includes Pydantic models for validating JSON webhook events. These models can be imported and used without instantiating the Jamf Pro client.

.. note::

    XML webhooks are not supported by the SDK.

Take this example ``ComputerAdded`` event:

.. code-block:: json

    {
        "webhook": {
            "eventTimestamp": 1685313891,
            "id": 1,
            "name": "New Computer Webhook",
            "webhookEvent": "ComputerAdded"
        },
        "event": {
            "alternateMacAddress": "00:67:31:80:18:80",
            "building": "",
            "department": "",
            "deviceName": "Zach's MacBook Pro",
            "emailAddress": "zach@example.org",
            "ipAddress": "118.36.18.147",
            "jssID": 2,
            "macAddress": "1c:bd:27:12:ad:6a",
            "model": "MacBookPro18,3",
            "osBuild": "22E772610a",
            "osVersion": "13.3.1 (a)",
            "phone": "690.741.7883x61304",
            "position": "Founder",
            "realName": "Zach",
            "reportedIpAddress": "188.51.118.97",
            "room": "",
            "serialNumber": "MSMDVUC1HB",
            "udid": "B6AC3528-474D-48A1-887C-7ABA3661C226",
            "userDirectoryID": "",
            "username": "zach"
        }
    }

It can be validated using the same name model, and then the fields accessed through dot notation (the same as the response objects from the Jamf Pro client).

    >>> import json
    >>> from jamf_pro_sdk.models.webhooks import ComputerAdded
    >>> event_data = json.loads(event_body)
    >>> validated_event = ComputerAdded(**event_data)
    >>> validated_event.webhook
    ComputerAddedWebhook(eventTimestamp=1685313891, id=1, name='New Computer Webhook', webhookEvent='ComputerAdded')
    >>> validated_event.event.ipAddress
    IPv4Address('118.36.18.147')
    >>>

