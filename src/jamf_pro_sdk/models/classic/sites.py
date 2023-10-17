from typing import Optional

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicSiteItem(BaseModel, extra=Extra.allow):
    """Represents a site record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_sites` operation.
    """

    id: Optional[int]
    name: Optional[str]


class ClassicSite(ClassicApiModel):
    """Represents a site record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_site_by_id` operation.

    Note that due to the simplicity of the model this information is available in the list.
    """

    _xml_root_name = "site"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name"}

    id: Optional[int]
    name: Optional[str]
