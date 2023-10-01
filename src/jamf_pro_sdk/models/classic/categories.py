from typing import Optional

from pydantic import Extra

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicCategoryItem(BaseModel, extra=Extra.allow):
    """Represents a category record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_categories` operation.
    """

    id: Optional[int]
    name: Optional[str]
    priority: Optional[int]


class ClassicCategory(ClassicApiModel):
    """Represents a category record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_category_by_id` operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, and ``priority. To bypass this
    behavior export the model using :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before
    pasting to the API operation.
    """

    _xml_root_name = "category"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "priority"}

    id: Optional[int]
    name: Optional[str]
    priority: Optional[int]
    