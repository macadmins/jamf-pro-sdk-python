from typing import Optional

from pydantic import ConfigDict

from .. import BaseModel
from . import ClassicApiModel

_XML_ARRAY_ITEM_NAMES = {}


class ClassicCategoriesItem(BaseModel):
    """Represents a category record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_all_categories` operation.
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None


class ClassicCategory(ClassicApiModel):
    """Represents a category record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_category_by_id` operation.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``name``, and ``priority``. To bypass this
    behavior export the model using :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before
    passing to the API operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "category"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"name", "priority"}

    id: Optional[int] = None
    name: Optional[str] = None
    priority: Optional[int] = None
