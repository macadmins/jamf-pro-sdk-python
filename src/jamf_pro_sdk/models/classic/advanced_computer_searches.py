from typing import List, Optional

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel, ClassicSite
from .criteria import ClassicCriterion

_XML_ARRAY_ITEM_NAMES = {
    "advanced_computer_searches": "advanced_computer_search",
    "computers": "computer",
    "display_fields": "display_field",
}


class ClassicAdvancedComputerSearchDisplayField(BaseModel, extra=Extra.allow):
    """ClassicAdvancedComputerSearch nested model: advanced_computer_search.display_fields.

    Display fields are additional data that are returned with the results of an advanced search.
    Note that the API field names are **not** the same as the display field names. Refer to the
    Jamf Pro UI for the supported names.
    """

    name: Optional[str]


class ClassicAdvancedComputerSearchMember(BaseModel, extra=Extra.allow):
    """ClassicAdvancedComputerSearch nested model: advanced_computer_search.computers.

    In addition to the ``id``, ``name``, and ``udid`` fields, any defined display fields will also
    appear with their values from the inventory record.
    """

    id: Optional[int]
    name: Optional[str]
    udid: Optional[str]


class ClassicAdvancedComputerSearchesItem(ClassicApiModel):
    """Represents an advanced computer search record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_all_advanced_computer_searches`
    operation.
    """

    id: Optional[int]
    name: Optional[str]


class ClassicAdvancedComputerSearch(ClassicApiModel):
    """Represents an advanced computer search record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_all_advanced_computer_searches`
    operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, ``site``, ``criteria``, and ``display_fields``. To bypass this behavior
    export the model using
    :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    _xml_root_name = "advanced_computer_search"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "site", "criteria", "display_fields"}

    id: Optional[int]
    name: Optional[str]
    site: Optional[ClassicSite]
    criteria: Optional[List[ClassicCriterion]]
    display_fields: Optional[List[ClassicAdvancedComputerSearchDisplayField]]
    computers: Optional[List[ClassicAdvancedComputerSearchMember]]
