from typing import Optional

from pydantic import Extra

from .. import BaseModel


class Script(BaseModel, extra=Extra.allow):
    """Represents a script record. The same data is
    returned for both GET scripts and GET script by ID."""

    id: Optional[int]
    name: Optional[str]
    info: Optional[str]
    notes: Optional[str]
    priority: Optional[str]
    parameter4: Optional[str]
    parameter5: Optional[str]
    parameter6: Optional[str]
    parameter7: Optional[str]
    parameter8: Optional[str]
    parameter9: Optional[str]
    parameter10: Optional[str]
    parameter11: Optional[str]
    osRequirements: Optional[str]
    scriptContents: Optional[str]
    categoryId: Optional[int]
    categoryName: Optional[str]
