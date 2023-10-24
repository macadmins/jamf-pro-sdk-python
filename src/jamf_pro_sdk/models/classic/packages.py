from typing import Optional, Union

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicPackageItem(BaseModel, extra=Extra.allow):
    """Represents a package record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_packages` operation.
    """

    id: Optional[int]
    name: Optional[str]


class ClassicPackage(ClassicApiModel):
    """Represents a package returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_package_by_id` operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``category``, ``filename``, ``info``, ``notes``, ``priority``,
    ``reboot_required``, ``os_requirements``, and ``install_if_reported_available``. To bypass this
    behavior export the model using :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before
    pasting to the API operation.
    """

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

    id: Optional[int]
    name: Optional[str]
    category: Optional[str]
    filename: Optional[str]
    info: Optional[str]
    notes: Optional[str]
    priority: Optional[int]
    reboot_required: Optional[bool]
    fill_user_template: Optional[bool]
    fill_existing_users: Optional[bool]
    allow_uninstalled: Optional[bool]
    os_requirements: Optional[str]
    required_processor: Optional[str]
    hash_type: Optional[str]
    hash_value: Optional[str]
    switch_with_package: Optional[str]
    install_if_reported_available: Optional[bool]
    reinstall_option: Optional[str]
    triggering_files: Optional[Union[dict, str]]
    send_notification: Optional[bool]
