from typing import Optional

from pydantic import ConfigDict

from .. import BaseModel


class Package(BaseModel):
    """Represents a full package record."""

    model_config = ConfigDict(extra="allow")

    id: Optional[str]
    packageName: str
    fileName: str
    categoryId: str
    info: Optional[str]
    notes: Optional[str]
    priority: int
    osRequirements: Optional[str]
    fillUserTemplate: bool
    indexed: bool
    fillExistingUsers: bool
    swu: bool
    rebootRequired: bool
    selfHealNotify: bool
    selfHealingAction: Optional[str]
    osInstall: bool
    serialNumber: Optional[str]
    parentPackageId: Optional[str]
    basePath: Optional[str]
    suppressUpdates: bool
    cloudTransferStatus: str
    ignoreConflicts: bool
    suppressFromDock: bool
    suppressEula: bool
    suppressRegistration: bool
    installLanguage: Optional[str]
    md5: Optional[str]
    sha256: Optional[str]
    hashType: Optional[str]
    hashValue: Optional[str]
    size: Optional[str]
    osInstallerVersion: Optional[str]
    manifest: Optional[str]
    manifestFileName: Optional[str]
    format: Optional[str]
