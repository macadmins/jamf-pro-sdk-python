from enum import Enum
from typing import List, Optional

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel, ClassicSite

_XML_ARRAY_ITEM_NAMES = {
    "criteria": "criterion",
    "computers": "computer",
    "computer_additions": "computer",
    "computer_deletions": "computer",
}


class ClassicComputerGroupCriterionAndOr(str, Enum):
    and_: str = "and"
    or_: str = "or"


class ClassicComputerGroupCriterionSearchType(str, Enum):
    """ComputerGroup nested model: computer_group.criteria.search_type

    .. attention::

        The supported search types are dependent on the field that is entered in ``name``.

    """

    is_: str = "is"
    is_not: str = "is not"
    like: str = "like"
    not_like: str = "not like"
    has: str = "has"
    does_not_have: str = "does not have"
    matches_regex: str = "matches regex"
    does_not_match_regex: str = "does not match regex"
    before_yyyy_mm_dd: str = "before (yyyy-mm-dd)"
    after_yyyy_mm_dd: str = "after (yyyy-mm-dd)"
    more_than_x_days_ago: str = "more than x days ago"
    less_than_x_days_ago: str = "less than x days ago"
    current: str = "current"
    not_current: str = "not current"
    greater_than: str = "greater than"
    less_than: str = "less than"
    greater_than_or_equal: str = "greater than or equal"
    less_than_or_equal: str = "less than or equal"


# class ClassicComputerGroupsItem(BaseModel, extra=Extra.allow):
#     """Represents a computer group record returned by the
#     :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_computer_groups` operation.
#     """
#
#     id: int
#     name: str
#     is_smart: bool


class ClassicComputerGroupCriterion(BaseModel, extra=Extra.allow):
    """ComputerGroup nested model: computer_group.criteria

    Only valid for smart groups (``is_smart == True``).
    """

    name: str
    priority: int
    and_or: ClassicComputerGroupCriterionAndOr
    search_type: ClassicComputerGroupCriterionSearchType
    value: str
    opening_paren: bool
    closing_paren: bool


class ClassicComputerGroupMember(BaseModel, extra=Extra.allow):
    """ComputerGroup nested model: computer_group.computers,
    computer_group.computer_additions, computer_group.computer_deletions
    """

    id: Optional[int]
    name: Optional[str]
    mac_address: Optional[str]
    alt_mac_address: Optional[str]
    serial_number: Optional[str]


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

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "is_smart", "site", "criteria"}

    id: Optional[int]
    name: Optional[str]
    is_smart: Optional[bool]
    site: Optional[ClassicSite]
    criteria: Optional[List[ClassicComputerGroupCriterion]]
    computers: Optional[List[ClassicComputerGroupMember]]


class ClassicComputerGroupMembershipUpdate(ClassicApiModel):
    """Represents a computer group membership update. This model is generated as a part of the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.update_static_computer_group_membership_by_id`
    operation.
    """

    _xml_root_name = "computer_group"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    computer_additions: Optional[List[ClassicComputerGroupMember]]
    computer_deletions: Optional[List[ClassicComputerGroupMember]]
