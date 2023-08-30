from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Extra


class NewFile(BaseModel, extra=Extra.allow):
    accessKeyID: str
    secretAccessKey: str
    sessionToken: str
    region: str
    expiration: datetime
    bucketName: str
    path: str
    uuid: UUID


class File(BaseModel, extra=Extra.allow):
    region: str
    fileName: str
    length: int
    md5: str
    sha3: str


class DownloadUrl(BaseModel, extra=Extra.allow):
    uri: str
