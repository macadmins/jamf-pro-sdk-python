from datetime import date, datetime  # date in models: 2019-01-01
from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict, Field

from .. import BaseModel
from . import V1Site

# Computer Extension Attribute Models


class ComputerExtensionAttributeDataType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DATE_TIME = "DATE_TIME"


class ComputerExtensionAttributeInputType(str, Enum):
    TEXT = "TEXT"
    POPUP = "POPUP"
    SCRIPT = "SCRIPT"
    LDAP = "LDAP"


class ComputerExtensionAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    definitionId: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    multiValue: Optional[bool] = None
    values: Optional[List[str]] = None
    dataType: Optional[ComputerExtensionAttributeDataType] = None
    options: Optional[List[str]] = None
    inputType: Optional[ComputerExtensionAttributeInputType] = None


# Computer General Models


class ComputerRemoteManagement(BaseModel):
    model_config = ConfigDict(extra="allow")

    managed: Optional[bool] = None
    managementUsername: Optional[str] = None
    managementPassword: Optional[str] = None


class ComputerMdmCapability(BaseModel):
    model_config = ConfigDict(extra="allow")

    capable: Optional[bool] = None
    capableUsers: Optional[List[str]] = None


class EnrollmentMethod(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    objectName: Optional[str] = None
    objectType: Optional[str] = None


class ComputerGeneral(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    lastIpAddress: Optional[str] = None
    lastReportedIp: Optional[str] = None
    jamfBinaryVersion: Optional[str] = None
    platform: Optional[str] = None
    barcode1: Optional[str] = None
    barcode2: Optional[str] = None
    assetTag: Optional[str] = None
    remoteManagement: Optional[ComputerRemoteManagement] = Field(
        default_factory=ComputerRemoteManagement
    )
    supervised: Optional[bool] = None
    mdmCapable: Optional[ComputerMdmCapability] = None
    reportDate: Optional[datetime] = None
    lastContactTime: Optional[datetime] = None
    lastCloudBackupDate: Optional[datetime] = None
    lastEnrolledDate: Optional[datetime] = None
    mdmProfileExpiration: Optional[datetime] = None
    initialEntryDate: Optional[date] = None  # 2018-10-31
    distributionPoint: Optional[str] = None
    enrollmentMethod: Optional[EnrollmentMethod] = None
    site: Optional[V1Site] = Field(default_factory=V1Site)
    itunesStoreAccountActive: Optional[bool] = None
    enrolledViaAutomatedDeviceEnrollment: Optional[bool] = None
    userApprovedMdm: Optional[bool] = None
    declarativeDeviceManagementEnabled: Optional[bool] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None
    managementId: Optional[str] = None


# Computer Disk Encryption Models


class ComputerPartitionFileVault2State(str, Enum):
    UNKNOWN = "UNKNOWN"
    UNENCRYPTED = "UNENCRYPTED"
    INELIGIBLE = "INELIGIBLE"
    DECRYPTED = "DECRYPTED"
    DECRYPTING = "DECRYPTING"
    ENCRYPTED = "ENCRYPTED"
    ENCRYPTING = "ENCRYPTING"
    RESTART_NEEDED = "RESTART_NEEDED"
    OPTIMIZING = "OPTIMIZING"
    DECRYPTING_PAUSED = "DECRYPTING_PAUSED"
    ENCRYPTING_PAUSED = "ENCRYPTING_PAUSED"


class IndividualRecoveryKeyValidityStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ComputerPartitionEncryption(BaseModel):
    model_config = ConfigDict(extra="allow")

    partitionName: Optional[str] = None
    partitionFileVault2State: Optional[ComputerPartitionFileVault2State] = None
    partitionFileVault2Percent: Optional[int] = None


class ComputerDiskEncryption(BaseModel):
    model_config = ConfigDict(extra="allow")

    bootPartitionEncryptionDetails: Optional[ComputerPartitionEncryption] = None
    individualRecoveryKeyValidityStatus: Optional[IndividualRecoveryKeyValidityStatus] = None
    institutionalRecoveryKeyPresent: Optional[bool] = None
    diskEncryptionConfigurationName: Optional[str] = None
    fileVault2EnabledUserNames: Optional[List[str]] = None
    fileVault2EligibilityMessage: Optional[str] = None


# Computer Purchase Model


class ComputerPurchase(BaseModel):
    model_config = ConfigDict(extra="allow")

    leased: Optional[bool] = None
    purchased: Optional[bool] = None
    poNumber: Optional[str] = None
    poDate: Optional[date] = None
    vendor: Optional[str] = None
    warrantyDate: Optional[date] = None
    appleCareId: Optional[str] = None
    leaseDate: Optional[date] = None
    purchasePrice: Optional[str] = None
    lifeExpectancy: Optional[int] = None
    purchasingAccount: Optional[str] = None
    purchasingContact: Optional[str] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None


# Computer Application Model


class ComputerApplication(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    path: Optional[str] = None
    version: Optional[str] = None
    macAppStore: Optional[bool] = None
    sizeMegabytes: Optional[int] = None
    bundleId: Optional[str] = None
    updateAvailable: Optional[bool] = None
    externalVersionId: Optional[str] = None


# Computer Storage Models


class PartitionType(str, Enum):
    BOOT = "BOOT"
    RECOVERY = "RECOVERY"
    OTHER = "OTHER"


class ComputerPartition(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    sizeMegabytes: Optional[int] = None
    availableMegabytes: Optional[int] = None
    partitionType: Optional[PartitionType] = None
    percentUsed: Optional[int] = None
    fileVault2State: Optional[ComputerPartitionFileVault2State] = None
    fileVault2ProgressPercent: Optional[int] = None
    lvmManaged: Optional[bool] = None


class ComputerDisk(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    device: Optional[str] = None
    model: Optional[str] = None
    revision: Optional[str] = None
    serialNumber: Optional[str] = None
    sizeMegabytes: Optional[int] = None
    smartStatus: Optional[str] = None
    type: Optional[str] = None
    partitions: Optional[List[ComputerPartition]] = None


class ComputerStorage(BaseModel):
    model_config = ConfigDict(extra="allow")

    bootDriveAvailableSpaceMegabytes: Optional[int] = None
    disks: Optional[List[ComputerDisk]] = None


# Computer User and Location Model


class ComputerUserAndLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: Optional[str] = None
    realname: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    departmentId: Optional[str] = None
    buildingId: Optional[str] = None
    room: Optional[str] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None


# Computer Configuration Profile Model


class ComputerConfigurationProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    username: Optional[str] = None
    lastInstalled: Optional[datetime] = None
    removable: Optional[bool] = None
    displayName: Optional[str] = None
    profileIdentifier: Optional[str] = None


# Computer Printer Model


class ComputerPrinter(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    location: Optional[str] = None


# Computer Service Model


class ComputerService(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None


# Computer Hardware Models


class ComputerHardware(BaseModel):
    model_config = ConfigDict(extra="allow")

    make: Optional[str] = None
    model: Optional[str] = None
    modelIdentifier: Optional[str] = None
    serialNumber: Optional[str] = None
    processorSpeedMhz: Optional[int] = None
    processorCount: Optional[int] = None
    coreCount: Optional[int] = None
    processorType: Optional[str] = None
    processorArchitecture: Optional[str] = None
    busSpeedMhz: Optional[int] = None
    cacheSizeKilobytes: Optional[int] = None
    networkAdapterType: Optional[str] = None
    macAddress: Optional[str] = None
    altNetworkAdapterType: Optional[str] = None
    altMacAddress: Optional[str] = None
    totalRamMegabytes: Optional[int] = None
    openRamSlots: Optional[int] = None
    batteryCapacityPercent: Optional[int] = None
    smcVersion: Optional[str] = None
    nicSpeed: Optional[str] = None
    opticalDrive: Optional[str] = None
    bootRom: Optional[str] = None
    bleCapable: Optional[bool] = None
    supportsIosAppInstalls: Optional[bool] = None
    appleSilicon: Optional[bool] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None


# Computer Local User Account Models


class UserAccountType(str, Enum):
    LOCAL = "LOCAL"
    MOBILE = "MOBILE"
    UNKNOWN = "UNKNOWN"


class AzureActiveDirectoryId(str, Enum):
    ACTIVATED = "ACTIVATED"
    DEACTIVATED = "DEACTIVATED"
    UNRESPONSIVE = "UNRESPONSIVE"
    UNKNOWN = "UNKNOWN"


class ComputerLocalUserAccount(BaseModel):
    model_config = ConfigDict(extra="allow")

    uid: Optional[str] = None
    username: Optional[str] = None
    fullName: Optional[str] = None
    admin: Optional[bool] = None
    homeDirectory: Optional[str] = None
    homeDirectorySizeMb: Optional[int] = None
    fileVault2Enabled: Optional[bool] = None
    userAccountType: Optional[UserAccountType] = None
    passwordMinLength: Optional[int] = None
    passwordMaxAge: Optional[int] = None
    passwordMinComplexCharacters: Optional[int] = None
    passwordHistoryDepth: Optional[int] = None
    passwordRequireAlphanumeric: Optional[bool] = None
    computerAzureActiveDirectoryId: Optional[str] = None
    userAzureActiveDirectoryId: Optional[str] = None
    azureActiveDirectoryId: Optional[AzureActiveDirectoryId] = None


# Computer Certificate Models


class LifecycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CertificateStatus(str, Enum):
    EXPIRING = "EXPIRING"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PENDING_REVOKE = "PENDING_REVOKE"
    ISSUED = "ISSUED"


class ComputerCertificate(BaseModel):
    model_config = ConfigDict(extra="allow")

    commonName: Optional[str] = None
    identity: Optional[bool] = None
    expirationDate: Optional[datetime] = None
    username: Optional[str] = None
    lifecycleStatus: Optional[LifecycleStatus] = None
    certificateStatus: Optional[CertificateStatus] = None
    subjectName: Optional[str] = None
    serialNumber: Optional[str] = None
    sha1Fingerprint: Optional[str] = None
    issuedDate: Optional[str] = None


# Computer Attachment Model


class ComputerAttachment(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    name: Optional[str] = None
    fileType: Optional[str] = None
    sizeBytes: Optional[int] = None


# Computer Plugin Model


class ComputerPlugin(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    version: Optional[str] = None
    path: Optional[str] = None


# Computer Package Receipt Model


class ComputerPackageReceipts(BaseModel):
    model_config = ConfigDict(extra="allow")

    installedByJamfPro: Optional[List[str]] = None
    installedByInstallerSwu: Optional[List[str]] = None
    cached: Optional[List[str]] = None


# Computer Font Model


class ComputerFont(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    version: Optional[str] = None
    path: Optional[str] = None


# Computer Security Models


class SipStatus(str, Enum):
    NOT_COLLECTED = "NOT_COLLECTED"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class GatekeeperStatus(str, Enum):
    NOT_COLLECTED = "NOT_COLLECTED"
    DISABLED = "DISABLED"
    APP_STORE_AND_IDENTIFIED_DEVELOPERS = "APP_STORE_AND_IDENTIFIED_DEVELOPERS"
    APP_STORE = "APP_STORE"


class SecureBootLevel(str, Enum):
    NO_SECURITY = "NO_SECURITY"
    MEDIUM_SECURITY = "MEDIUM_SECURITY"
    FULL_SECURITY = "FULL_SECURITY"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    UNKNOWN = "UNKNOWN"


class ExternalBootLevel(str, Enum):
    ALLOW_BOOTING_FROM_EXTERNAL_MEDIA = "ALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA = "DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    UNKNOWN = "UNKNOWN"


class ComputerSecurity(BaseModel):
    model_config = ConfigDict(extra="allow")

    sipStatus: Optional[SipStatus] = None
    gatekeeperStatus: Optional[GatekeeperStatus] = None
    xprotectVersion: Optional[str] = None
    autoLoginDisabled: Optional[bool] = None
    remoteDesktopEnabled: Optional[bool] = None
    activationLockEnabled: Optional[bool] = None
    recoveryLockEnabled: Optional[bool] = None
    firewallEnabled: Optional[bool] = None
    secureBootLevel: Optional[SecureBootLevel] = None
    externalBootLevel: Optional[ExternalBootLevel] = None
    bootstrapTokenAllowed: Optional[bool] = None


# Computer Operating System Models


class FileVault2Status(str, Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_ENCRYPTED = "NOT_ENCRYPTED"
    BOOT_ENCRYPTED = "BOOT_ENCRYPTED"
    SOME_ENCRYPTED = "SOME_ENCRYPTED"
    ALL_ENCRYPTED = "ALL_ENCRYPTED"


class ComputerOperatingSystem(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    version: Optional[str] = None
    build: Optional[str] = None
    activeDirectoryStatus: Optional[str] = None
    fileVault2Status: Optional[FileVault2Status] = None
    softwareUpdateDeviceId: Optional[str] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None


# Computer Licensed Software Model


class ComputerLicensedSoftware(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    name: Optional[str] = None


# Computer iBeacon Model


class ComputeriBeacon(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None


# Computer Software Update Model


class ComputerSoftwareUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    version: Optional[str] = None
    packageName: Optional[str] = None


# Computer Content Caching Models


class ComputerContentCachingParentAlert(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentAlertId: Optional[str] = None
    addresses: Optional[List[str]] = None
    className: Optional[str] = None
    postDate: Optional[datetime] = None


class ComputerContentCachingParentCapabilities(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentCapabilitiesId: Optional[str] = None
    imports: Optional[bool] = None
    namespaces: Optional[bool] = None
    personalContent: Optional[bool] = None
    queryParameters: Optional[bool] = None
    sharedContent: Optional[bool] = None
    prioritization: Optional[bool] = None


class ComputerContentCachingParentLocalNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentLocalNetworkId: Optional[str] = None
    speed: Optional[int] = None
    wired: Optional[bool] = None


class ComputerContentCachingParentDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentDetailsId: Optional[str] = None
    acPower: Optional[bool] = None
    cacheSizeBytes: Optional[int] = None
    capabilities: Optional[ComputerContentCachingParentCapabilities] = None
    portable: Optional[bool] = None
    localNetwork: Optional[List[ComputerContentCachingParentLocalNetwork]] = None


class ComputerContentCachingParent(BaseModel):
    model_config = ConfigDict(extra="allow")

    contentCachingParentId: Optional[str] = None
    address: Optional[str] = None
    alerts: Optional[ComputerContentCachingParentAlert] = None
    details: Optional[ComputerContentCachingParentDetails] = None
    guid: Optional[str] = None
    healthy: Optional[bool] = None
    port: Optional[int] = None
    version: Optional[str] = None


class ComputerContentCachingAlert(BaseModel):
    model_config = ConfigDict(extra="allow")

    cacheBytesLimit: Optional[int] = None
    className: Optional[str] = None
    pathPreventingAccess: Optional[str] = None
    postDate: Optional[datetime] = None
    reservedVolumeBytes: Optional[int] = None
    resource: Optional[str] = None


class ComputerContentCachingCacheDetail(BaseModel):
    model_config = ConfigDict(extra="allow")

    computerContentCachingCacheDetailsId: Optional[str] = None
    categoryName: Optional[str] = None
    diskSpaceBytesUsed: Optional[int] = None


class ComputerContentCachingDataMigrationErrorUserInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    key: Optional[str] = None
    value: Optional[str] = None


class ComputerContentCachingDataMigrationError(BaseModel):
    model_config = ConfigDict(extra="allow")

    code: Optional[int] = None
    domain: Optional[str] = None
    userInfo: Optional[List[ComputerContentCachingDataMigrationErrorUserInfo]] = None


class ComputerContentCachingRegistrationStatus(str, Enum):
    CONTENT_CACHING_FAILED = "CONTENT_CACHING_FAILED"
    CONTENT_CACHING_PENDING = "CONTENT_CACHING_PENDING"
    CONTENT_CACHING_SUCCEEDED = "CONTENT_CACHING_SUCCEEDED"


class ComputerContentCachingTetheratorStatus(str, Enum):
    CONTENT_CACHING_UNKNOWN = "CONTENT_CACHING_UNKNOWN"
    CONTENT_CACHING_DISABLED = "CONTENT_CACHING_DISABLED"
    CONTENT_CACHING_ENABLED = "CONTENT_CACHING_ENABLED"


class ComputerContentCaching(BaseModel):
    model_config = ConfigDict(extra="allow")

    computerContentCachingInformationId: Optional[str] = None
    parents: Optional[List[ComputerContentCachingParent]] = None
    alerts: Optional[List[ComputerContentCachingAlert]] = None
    activated: Optional[bool] = None
    active: Optional[bool] = None
    actualCacheBytesUsed: Optional[int] = None
    cacheDetails: Optional[List[ComputerContentCachingCacheDetail]] = None
    cacheBytesFree: Optional[int] = None
    cacheBytesLimit: Optional[int] = None
    cacheStatus: Optional[str] = None
    cacheBytesUsed: Optional[int] = None
    dataMigrationCompleted: Optional[bool] = None
    dataMigrationProgressPercentage: Optional[int] = None
    dataMigrationError: Optional[ComputerContentCachingDataMigrationError] = None
    maxCachePressureLast1HourPercentage: Optional[int] = None
    personalCacheBytesFree: Optional[int] = None
    personalCacheBytesLimit: Optional[int] = None
    personalCacheBytesUsed: Optional[int] = None
    port: Optional[int] = None
    publicAddress: Optional[str] = None
    registrationError: Optional[str] = None
    registrationResponseCode: Optional[int] = None
    registrationStarted: Optional[datetime] = None
    registrationStatus: Optional[ComputerContentCachingRegistrationStatus] = None
    restrictedMedia: Optional[bool] = None
    serverGuid: Optional[str] = None
    startupStatus: Optional[str] = None
    tetheratorStatus: Optional[ComputerContentCachingTetheratorStatus] = None
    totalBytesAreSince: Optional[datetime] = None
    totalBytesDropped: Optional[int] = None
    totalBytesImported: Optional[int] = None
    totalBytesReturnedToChildren: Optional[int] = None
    totalBytesReturnedToClients: Optional[int] = None
    totalBytesReturnedToPeers: Optional[int] = None
    totalBytesStoredFromOrigin: Optional[int] = None
    totalBytesStoredFromParents: Optional[int] = None
    totalBytesStoredFromPeers: Optional[int] = None


# Computer Group Membership Model


class ComputerGroupMembership(BaseModel):
    model_config = ConfigDict(extra="allow")

    groupId: Optional[str] = None
    groupName: Optional[str] = None
    smartGroup: Optional[bool] = None


# Computer Inventory Model


class Computer(BaseModel):
    """Represents a full computer inventory record."""

    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    udid: Optional[str] = None
    general: Optional[ComputerGeneral] = Field(default_factory=ComputerGeneral)
    diskEncryption: Optional[ComputerDiskEncryption] = None
    purchasing: Optional[ComputerPurchase] = None
    applications: Optional[List[ComputerApplication]] = None
    storage: Optional[ComputerStorage] = None
    userAndLocation: Optional[ComputerUserAndLocation] = Field(
        default_factory=ComputerUserAndLocation
    )
    configurationProfiles: Optional[List[ComputerConfigurationProfile]] = None
    printers: Optional[List[ComputerPrinter]] = None
    services: Optional[List[ComputerService]] = None
    hardware: Optional[ComputerHardware] = None
    localUserAccounts: Optional[List[ComputerLocalUserAccount]] = None
    certificates: Optional[List[ComputerCertificate]] = None
    attachments: Optional[List[ComputerAttachment]] = None
    plugins: Optional[List[ComputerPlugin]] = None
    packageReceipts: Optional[ComputerPackageReceipts] = None
    fonts: Optional[List[ComputerFont]] = None
    security: Optional[ComputerSecurity] = None
    operatingSystem: Optional[ComputerOperatingSystem] = None
    licensedSoftware: Optional[List[ComputerLicensedSoftware]] = None
    ibeacons: Optional[List[ComputeriBeacon]] = None
    softwareUpdates: Optional[List[ComputerSoftwareUpdate]] = None
    extensionAttributes: Optional[List[ComputerExtensionAttribute]] = None
    contentCaching: Optional[ComputerContentCaching] = None
    groupMemberships: Optional[List[ComputerGroupMembership]] = None
