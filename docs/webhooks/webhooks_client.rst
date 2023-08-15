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
    >>> md_enroll = get_webhook_generator(MobileDeviceEnrolled)
    >>> md_enroll
    <class 'abc.MobileDeviceEnrolledGenerator'>
    >>> md1 = md_enroll.build()
    >>> md1.webhook
    MobileDeviceEnrolledWebhook(eventTimestamp=1685331210, id=1031, name='JYksqLwBskpOmWTXLVJZ', webhookEvent='MobileDeviceEnrolled')
    >>>

Each time

    >>> from jamf_pro_sdk.clients.webhooks import get_webhook_generator
    >>> from jamf_pro_sdk.models.webhooks import MobileDeviceEnrolled
    >>> md_enroll = get_webhook_generator(MobileDeviceEnrolled)
    >>> md_enroll
    <class 'abc.MobileDeviceEnrolledGenerator'>
    >>> md1 = md_enroll.build()
    >>> md1.webhook
    MobileDeviceEnrolledWebhook(eventTimestamp=1685331210, id=1031, name='JYksqLwBskpOmWTXLVJZ', webhookEvent='MobileDeviceEnrolled')
    >>>

Each time

    >>> from jamf_pro_sdk.clients.webhooks import get_webhook_generator
    >>> from jamf_pro_sdk.models.webhooks import MobileDeviceEnrolled
    >>> md_enroll = get_webhook_generator(MobileDeviceEnrolled)
    >>> md_enroll
    <class 'abc.MobileDeviceEnrolledGenerator'>
    >>> md1 = md_enroll.build()
    >>> md1.webhook
    MobileDeviceEnrolledWebhook(eventTimestamp=1685331210, id=1031, name='JYksqLwBskpOmWTXLVJZ', webhookEvent='MobileDeviceEnrolled')
    >>>

Each time ``build()`` is used with a generator a unique webhook object is returned.

The webhooks client accepts a model as an argument to the ``fire()`` method and will create a generator internally. A unique JSON payload will then be sent to provided URL using HTTP POST.

    >>> from jamf_pro_sdk.clients.webhooks import WebhooksClient
    >>> client = WebhooksClient("http://localhost/post")
    >>> client.fire(MobileDeviceEnrolled)
    >>>

The client automatically handles concurrency with a default of 10 workers. Passing a counter higher than 1 will automatically multi-thread requests. Each HTTP POST will contain a unique JSON payload.

    >>> client.fire(MobileDeviceEnrolled, 100)
