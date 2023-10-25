from typing import Optional

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {"starting_address": "starting_address", "ending_address": "ending_address"}


class ClassicNetworkSegmentItem(BaseModel, extra=Extra.allow):
    """Represents a network_segment record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_network_segments` operation.
    """

    id: Optional[int]
    name: Optional[str]
    starting_address: Optional[str]
    ending_address: Optional[str]


class ClassicNetworkSegment(ClassicApiModel):
    """Represents a network_segment record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_network_segment_by_id` operation.
    """

    _xml_root_name = "network_segment"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {
        "name",
        "starting_address",
        "ending_address",
        "distribution_server",
        "distribution_point",
        "url",
        "swu_server",
        "building",
        "department",
        "override_buildings",
        "override_departments",
    }

    id: Optional[int]
    name: Optional[str]
    starting_address: Optional[str]
    ending_address: Optional[str]
    distribution_server: Optional[str]
    distribution_point: Optional[str]
    url: Optional[str]
    swu_server: Optional[str]
    building: Optional[str]
    department: Optional[str]
    override_buildings: Optional[bool]
    override_departments: Optional[bool]
