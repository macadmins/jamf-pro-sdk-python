Webhook Receiver Example using FastAPI
======================================

The SDK's webhook models use Pydantic which is compatible with FastAPI for request validation.

Installation Requirements
-------------------------

.. code-block:: console

    (.venv) % pip install fastapi 'uvicorn[standard]'

The App
-------

Create a file called ``main.py`` and copy the contents below.

This is a basic webhook receiver that only processes mobile device enrollment events. There is a single route at the root of the server ``/`` that will accept HTTP POST requests with JSON bodies. JSON is the default input/output for FastAPI apps and there is no extra configuration needed. The use of ``typing.Union`` allows multiple models to be accepted for the route.

.. code-block:: python

    from typing import Union

    from fastapi import FastAPI
    from jamf_pro_sdk.models.webhooks import MobileDeviceEnrolled, MobileDeviceUnEnrolled

    app = FastAPI()

    AllowedWebhooks = Union[MobileDeviceEnrolled, MobileDeviceUnEnrolled]


    @app.post("/")
    def receive_webhook(webhook: AllowedWebhooks):
        print(f"Webhook received for device {webhook.event.udid}")


To learn more about FastAPI read the `First Steps <https://fastapi.tiangolo.com/tutorial/first-steps/>`_ tutorial.

Run the App
-----------

The ``uvicorn`` command will run the server. Using ``0.0.0.0`` will allow access using the IP address of the host running the app. To only test locally use ``127.0.0.1``.

.. code-block:: console

    (.venv) % uvicorn main:app --host 0.0.0.0 --port 80
    INFO:     Started server process [71338]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)

Test Using Webhooks Client
--------------------------

Now that the receiver is running you can send test events using the wehooks client.

    >>> from jamf_pro_sdk.clients.webhooks import WebhooksClient
    >>> from jamf_pro_sdk.models.webhooks import ComputerAdded, MobileDeviceEnrolled
    >>> client = WebhooksClient("http://0.0.0.0/")
    >>> client.fire(MobileDeviceEnrolled)
    >>> client.fire(ComputerAdded)

In the logs for the receiver you will see the requests being processed.

.. code-block:: console

    Webhook received for device 6A331227-7BC9-44CD-901F-D719F460CE21
    INFO:     127.0.0.1:63139 - "POST / HTTP/1.1" 200 OK
    INFO:     127.0.0.1:63139 - "POST / HTTP/1.1" 422 Unprocessable Entity

Note that the ``ComputerAdded`` event was rejected. Use of models for validation will ensure only allowed and correctly formatted webhook events are processed by the server.
