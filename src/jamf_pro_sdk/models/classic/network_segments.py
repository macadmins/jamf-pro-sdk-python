from typing import Optional

from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicNetworkSegmentItem(BaseModel):
    """Represents a network_segment record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_network_segments` operation.
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None
    starting_address: Optional[str] = None
    ending_address: Optional[str] = None


class ClassicNetworkSegment(ClassicApiModel):
    """Represents a network_segment record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_network_segment_by_id` operation.
    """

    model_config = ConfigDict(extra="allow")

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

    id: Optional[int] = None
    name: Optional[str] = None
    starting_address: Optional[str] = None
    ending_address: Optional[str] = None
    distribution_server: Optional[str] = None
    distribution_point: Optional[str] = None
    url: Optional[str] = None
    swu_server: Optional[str] = None
    building: Optional[str] = None
    department: Optional[str] = None
    override_buildings: Optional[bool] = None
    override_departments: Optional[bool] = None
