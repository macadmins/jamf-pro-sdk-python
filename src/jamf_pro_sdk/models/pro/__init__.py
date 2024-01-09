from typing import Optional

from pydantic import BaseModel


class V1Site(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
