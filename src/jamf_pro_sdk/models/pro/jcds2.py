from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NewFile(BaseModel):
    model_config = ConfigDict(extra="allow")

    accessKeyID: str
    secretAccessKey: str
    sessionToken: str
    region: str
    expiration: datetime
    bucketName: str
    path: str
    uuid: UUID


class File(BaseModel):
    model_config = ConfigDict(extra="allow")

    region: str
    fileName: str
    length: int
    md5: str
    sha3: str


class DownloadUrl(BaseModel):
    model_config = ConfigDict(extra="allow")

    uri: str
