from typing import List, Optional

from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel, ClassicSite
from .criteria import ClassicCriterion

_XML_ARRAY_ITEM_NAMES = {
    "criteria": "criterion",
    "computers": "computer",
    "computer_additions": "computer",
    "computer_deletions": "computer",
}


# class ClassicComputerGroupsItem(BaseModel, extra=Extra.allow):
#     """Represents a computer group record returned by the
#     :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_computer_groups` operation.
#     """
#
#     id: int
#     name: str
#     is_smart: bool


class ClassicComputerGroupMember(BaseModel):
    """ComputerGroup nested model: computer_group.computers,
    computer_group.computer_additions, computer_group.computer_deletions
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None
    mac_address: Optional[str] = None
    alt_mac_address: Optional[str] = None
    serial_number: Optional[str] = None


class ClassicComputerGroup(ClassicApiModel):
    """Represents a computer group record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_computer_groups` and
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_computer_group_by_id`
    operations.

    When returned by ``list_computer_groups`` only ``id``, ``name`` and ``is_smart`` will
    be populated.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``is_smart``, ``site``, and ``criteria``. To bypass this behavior
    export the model using
    :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "is_smart", "site", "criteria"}

    id: Optional[int] = None
    name: Optional[str] = None
    is_smart: Optional[bool] = None
    site: Optional[ClassicSite] = None
    criteria: Optional[List[ClassicCriterion]] = None
    computers: Optional[List[ClassicComputerGroupMember]] = None


class ClassicComputerGroupMembershipUpdate(ClassicApiModel):
    """Represents a computer group membership update. This model is generated as a part of the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.update_static_computer_group_membership_by_id`
    operation.
    """

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    computer_additions: Optional[List[ClassicComputerGroupMember]] = None
    computer_deletions: Optional[List[ClassicComputerGroupMember]] = None
