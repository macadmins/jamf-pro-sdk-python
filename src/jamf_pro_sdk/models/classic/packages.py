from typing import Optional, Union

from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES: dict = {}


class ClassicPackageItem(BaseModel):
    """Represents a package record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_packages` operation.
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None


class ClassicPackage(ClassicApiModel):
    """Represents a package returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_package_by_id` operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``category``, ``filename``, ``info``, ``notes``, ``priority``,
    ``reboot_required``, ``os_requirements``, and ``install_if_reported_available``. To bypass this
    behavior export the model using :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before
    pasting to the API operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "package"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {
        "name",
        "category",
        "filename",
        "info",
        "notes",
        "priority",
        "reboot_required",
        "os_requirements",
        "install_if_reported_available",
    }

    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    filename: Optional[str] = None
    info: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[int] = None
    reboot_required: Optional[bool] = None
    fill_user_template: Optional[bool] = None
    fill_existing_users: Optional[bool] = None
    allow_uninstalled: Optional[bool] = None
    os_requirements: Optional[str] = None
    required_processor: Optional[str] = None
    hash_type: Optional[str] = None
    hash_value: Optional[str] = None
    switch_with_package: Optional[str] = None
    install_if_reported_available: Optional[bool] = None
    reinstall_option: Optional[str] = None
    triggering_files: Optional[Union[dict, str]] = None
    send_notification: Optional[bool] = None
