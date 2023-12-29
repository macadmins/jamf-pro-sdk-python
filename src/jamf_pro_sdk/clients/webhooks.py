import concurrent.futures
import inspect
import random
import string
import time
import uuid
from functools import lru_cache
from typing import Iterator, Type, Union, cast

import requests
import requests.adapters

try:
    from faker import Faker
    from polyfactory import Use
    from polyfactory.factories.pydantic_factory import ModelFactory
except ImportError:
    raise ImportError("The 'webhooks' extra dependency is required.")

from ..models.webhooks import webhooks

WebhookGenerator = ModelFactory


class WebhooksClient:
    def __init__(
        self,
        url: str,
        max_concurrency: int = 10,
    ):
        """A client for simulating webhooks to an HTTP server.

        :param url: The full URL the client will send webhooks to. Include the scheme, port, and path.
        :type url: str

        :param max_concurrency: The maximum number of connections the client will make when sending
            webhooks to the given URL (defaults to `10`).
        :type max_concurrency: int
        """
        self.url = url
        self.max_concurrency = max_concurrency
        self.session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=max_concurrency, pool_maxsize=max_concurrency
        )
        self.session.mount(prefix="http://", adapter=adapter)
        self.session.mount(prefix="https://", adapter=adapter)

    @staticmethod
    def _batch(
        generator: Union[WebhookGenerator, Type[WebhookGenerator]], count: int
    ) -> Iterator[webhooks.WebhookModel]:
        for _ in range(count):
            yield generator.build()

    def send_webhook(self, webhook: webhooks.WebhookModel) -> requests.Response:
        """Send a single webhook in an HTTP POST request to the configured URL.

        :param webhook: The webhook object that will be serialized to JSON.
        :type webhook: ~webhooks.WebhookModel

        :return: `Requests Response <https://requests.readthedocs.io/en/latest/api/#requests.Response>`_ object
        :rtype: requests.Response
        """
        response = self.session.post(
            self.url, headers={"Content-Type": "application/json"}, data=webhook.model_dump_json()
        )
        return response

    def fire(
        self,
        webhook: Type[webhooks.WebhookModel],
        count: int = 1,
    ) -> Iterator[requests.Response]:
        """Send one or more randomized webhooks to the configured URL using a webhook model. This
        method will automatically make the requests concurrently up to the configured max concurrency.

        :param webhook: A webhook model. This must be the ``type`` and not an instantiated object.
        :type webhook: Type[webhooks.WebhookModel]

        :param count: The number of webhook events to send (defaults to `1`).
        :type count: int

        :return: An iterator that will yield
            `Requests Response <https://requests.readthedocs.io/en/latest/api/#requests.Response>`_ object
            objects.
        :rtype: Iterator[requests.Response]
        """
        generator = get_webhook_generator(webhook)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
            executor_results = executor.map(
                self.send_webhook, self._batch(generator=generator, count=count)
            )

        for result in executor_results:
            yield result


def epoch() -> int:
    """Returns epoch as an integer."""
    return int(time.time())


def serial_number() -> str:
    """Returns a randomized string representing an Apple serial number."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def udid() -> str:
    """Returns an upper-cased UUID."""
    return str(uuid.uuid4()).upper()


@lru_cache
def get_webhook_generator(model: Type[webhooks.WebhookModel], **kwargs) -> Type[WebhookGenerator]:
    """Returns a webhook generator for the given webhook model. Generators are wrappers around
    webhook models to create mock data.

    The returned generator is cached and will be returned for any future calls for the same model.

    :param model: A webhook model. This must be the ``type`` and not an instantiated object.
    :type model: Type[webhooks.WebhookModel]
    """
    if not kwargs:
        kwargs = {}

    return cast(
        "Type[WebhookGenerator]",
        type(model.__name__ + "Generator", (WebhookGenerator,), {"__model__": model, **kwargs}),
    )


def _load_webhook_generators():
    """The following code runs when the file is imported. All webhook models discovered (that is,
    any class based from ``WebhookModel``) will be processed to set up mock data generation for key
    fields. The returned generator is then loaded into the ``globals()`` so they can be referenced
    by other models that depend on them (ensuring the fields configured for mock data are intact).
    """
    for name, cls in webhooks.__dict__.items():
        if not inspect.isclass(cls) or not issubclass(cls, webhooks.WebhookModel):
            continue

        attrs: dict = {"__set_as_default_factory_for_type__": True, "__faker__": Faker()}

        if issubclass(cls, webhooks.WebhookData):
            attrs["eventTimestamp"] = Use(epoch)

        elif issubclass(cls, webhooks.WebhookModel):
            if "macAddress" in cls.model_fields:
                attrs["macAddress"] = attrs["__faker__"].mac_address
            if "alternateMacAddress" in cls.model_fields:
                attrs["alternateMacAddress"] = attrs["__faker__"].mac_address
            if "wifiMacAddress" in cls.model_fields:
                attrs["wifiMacAddress"] = attrs["__faker__"].mac_address
            if "bluetoothMacAddress" in cls.model_fields:
                attrs["bluetoothMacAddress"] = attrs["__faker__"].mac_address

            if "udid" in cls.model_fields:
                attrs["udid"] = Use(udid)
            if "serialNumber" in cls.model_fields:
                attrs["serialNumber"] = Use(serial_number)

            # TODO: Fields that are specific to iOS/iPadOS devices
            # if "icciID" in cls.__fields__:
            #     kwargs["icciID"] = Use(icci_id)
            # if "imei" in cls.__fields__:
            #     kwargs["imei"] = Use(imei)

            if "realName" in cls.model_fields:
                attrs["realName"] = attrs["__faker__"].name
            if "username" in cls.model_fields:
                attrs["username"] = attrs["__faker__"].user_name
            if "emailAddress" in cls.model_fields:
                attrs["emailAddress"] = attrs["__faker__"].ascii_safe_email
            if "phone" in cls.model_fields:
                attrs["phone"] = attrs["__faker__"].phone_number

        w = get_webhook_generator(cls, **attrs)
        globals()[w.__name__] = w


_load_webhook_generators()
