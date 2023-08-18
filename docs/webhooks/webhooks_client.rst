Basic Usage: Webhooks Client
============================

The webhooks client allows developers to send test events with randomized data to their applications. These events are derived from the webhook models in the SDK.

Installation Requirements
-------------------------

The webhook generator requires additional dependencies not included with the default installation of the SDK.

.. code-block:: console

    (.venv) % pip install 'jamf-pro-sdk[webhooks]'

Basic Usage
-----------

The webhooks client provides an interface to create generator classes to create mock data. Generators are wrappers around webhook models.

    >>> from jamf_pro_sdk.clients.webhooks import get_webhook_generator
    >>> from jamf_pro_sdk.models.webhooks import MobileDeviceEnrolled
    >>> mobile_device_enrolled_generator = get_webhook_generator(MobileDeviceEnrolled)
    >>> mobile_device_enrolled_generator
    <class 'abc.MobileDeviceEnrolledGenerator'>
    >>> mobile_device_1 = mobile_device_enrolled_generator.build()
    >>> mobile_device_1.webhook
    MobileDeviceEnrolledWebhook(eventTimestamp=1685331210, id=1031, name='JYksqLwBskpOmWTXLVJZ', webhookEvent='MobileDeviceEnrolled')
    >>>

Each time ``build()`` is used with a generator a unique webhook object is returned. These can be passed to the webhooks client and sent to a remote host mocking an actual Jamf Pro event.

    >>> from jamf_pro_sdk.clients.webhooks import WebhooksClient, get_webhook_generator
    >>> from jamf_pro_sdk.models.webhooks import ComputerCheckIn
    >>> computer_checkin_generator = get_webhook_generator(ComputerCheckIn)
    >>> client = WebhooksClient("http://localhost/post")
    >>> for _ in range(3):
    ...     client.send_webhook(computer_checkin_generator.build())
    ...
    <Response [200]>
    <Response [200]>
    <Response [200]>
    >>>

The client also has a ``fire()`` method that can send many events rapidly. The webhooks client accepts a model type as an argument to the ``fire()`` method and will create a generator internally. A unique JSON payload will then be sent to provided URL using HTTP POST.

    >>> from jamf_pro_sdk.clients.webhooks import WebhooksClient
    >>> client = WebhooksClient("http://localhost/post")
    >>> list(client.fire(MobileDeviceEnrolled, 10))
    [<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>]
    >>>

The client automatically handles concurrency with a default of 10 threads. Passing a counter higher than 1 will automatically multi-thread requests. Each HTTP POST will contain a unique JSON payload. Note that ``fire()`` returns an iterator.
