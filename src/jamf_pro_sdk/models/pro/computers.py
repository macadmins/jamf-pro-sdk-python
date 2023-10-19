from datetime import date, datetime  # date in models: 2019-01-01
from enum import Enum
from typing import List, Optional

from pydantic import Extra, Field

from .. import BaseModel
from . import V1Site

# Computer Extension Attribute Models


class ComputerExtensionAttributeDataType(str, Enum):
    STRING: str = "STRING"
    INTEGER: str = "INTEGER"
    DATE_TIME: str = "DATE_TIME"


class ComputerExtensionAttributeInputType(Enum):
    TEXT: str = "TEXT"
    POPUP: str = "POPUP"
    SCRIPT: str = "SCRIPT"
    LDAP: str = "LDAP"


class ComputerExtensionAttribute(BaseModel, extra=Extra.allow):
    definitionId: Optional[str]
    name: Optional[str]
    description: Optional[str]
    enabled: Optional[bool]
    multiValue: Optional[bool]
    values: Optional[List[str]]
    dataType: Optional[ComputerExtensionAttributeDataType]
    options: Optional[List[str]]
    inputType: Optional[ComputerExtensionAttributeInputType]


# Computer General Models


class ComputerRemoteManagement(BaseModel, extra=Extra.allow):
    managed: Optional[bool]
    managementUsername: Optional[str]
    managementPassword: Optional[str]


class ComputerMdmCapability(BaseModel, extra=Extra.allow):
    capable: Optional[bool]
    capableUsers: Optional[List[str]]


class EnrollmentMethod(BaseModel, extra=Extra.allow):
    id: Optional[str]
    objectName: Optional[str]
    objectType: Optional[str]


class ComputerGeneral(BaseModel, extra=Extra.allow):
    name: Optional[str]
    lastIpAddress: Optional[str]
    lastReportedIp: Optional[str]
    jamfBinaryVersion: Optional[str]
    platform: Optional[str]
    barcode1: Optional[str]
    barcode2: Optional[str]
    assetTag: Optional[str]
    remoteManagement: Optional[ComputerRemoteManagement] = Field(
        default_factory=ComputerRemoteManagement
    )
    supervised: Optional[bool]
    mdmCapable: Optional[ComputerMdmCapability]
    reportDate: Optional[datetime]
    lastContactTime: Optional[datetime]
    lastCloudBackupDate: Optional[datetime]
    lastEnrolledDate: Optional[datetime]
    mdmProfileExpiration: Optional[datetime]
    initialEntryDate: Optional[date]  # 2018-10-31
    distributionPoint: Optional[str]
    enrollmentMethod: Optional[EnrollmentMethod]
    site: Optional[V1Site] = Field(default_factory=V1Site)
    itunesStoreAccountActive: Optional[bool]
    enrolledViaAutomatedDeviceEnrollment: Optional[bool]
    userApprovedMdm: Optional[bool]
    declarativeDeviceManagementEnabled: Optional[bool]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]
    managementId: Optional[str]


# Computer Disk Encryption Models


class ComputerPartitionFileVault2State(str, Enum):
    UNKNOWN: str = "UNKNOWN"
    UNENCRYPTED: str = "UNENCRYPTED"
    INELIGIBLE: str = "INELIGIBLE"
    DECRYPTED: str = "DECRYPTED"
    DECRYPTING: str = "DECRYPTING"
    ENCRYPTED: str = "ENCRYPTED"
    ENCRYPTING: str = "ENCRYPTING"
    RESTART_NEEDED: str = "RESTART_NEEDED"
    OPTIMIZING: str = "OPTIMIZING"
    DECRYPTING_PAUSED: str = "DECRYPTING_PAUSED"
    ENCRYPTING_PAUSED: str = "ENCRYPTING_PAUSED"


class IndividualRecoveryKeyValidityStatus(str, Enum):
    VALID: str = "VALID"
    INVALID: str = "INVALID"
    UNKNOWN: str = "UNKNOWN"
    NOT_APPLICABLE: str = "NOT_APPLICABLE"


class ComputerPartitionEncryption(BaseModel, extra=Extra.allow):
    partitionName: Optional[str]
    partitionFileVault2State: Optional[ComputerPartitionFileVault2State]
    partitionFileVault2Percent: Optional[int]


class ComputerDiskEncryption(BaseModel, extra=Extra.allow):
    bootPartitionEncryptionDetails: Optional[ComputerPartitionEncryption]
    individualRecoveryKeyValidityStatus: Optional[IndividualRecoveryKeyValidityStatus]
    institutionalRecoveryKeyPresent: Optional[bool]
    diskEncryptionConfigurationName: Optional[str]
    fileVault2EnabledUserNames: Optional[List[str]]
    fileVault2EligibilityMessage: Optional[str]


# Computer Purchase Model


class ComputerPurchase(BaseModel, extra=Extra.allow):
    leased: Optional[bool]
    purchased: Optional[bool]
    poNumber: Optional[str]
    poDate: Optional[date]
    vendor: Optional[str]
    warrantyDate: Optional[date]
    appleCareId: Optional[str]
    leaseDate: Optional[date]
    purchasePrice: Optional[str]
    lifeExpectancy: Optional[int]
    purchasingAccount: Optional[str]
    purchasingContact: Optional[str]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]


# Computer Application Model


class ComputerApplication(BaseModel, extra=Extra.allow):
    name: Optional[str]
    path: Optional[str]
    version: Optional[str]
    macAppStore: Optional[bool]
    sizeMegabytes: Optional[int]
    bundleId: Optional[str]
    updateAvailable: Optional[bool]
    externalVersionId: Optional[str]


# Computer Storage Models


class PartitionType(str, Enum):
    BOOT: str = "BOOT"
    RECOVERY: str = "RECOVERY"
    OTHER: str = "OTHER"


class ComputerPartition(BaseModel, extra=Extra.allow):
    name: Optional[str]
    sizeMegabytes: Optional[int]
    availableMegabytes: Optional[int]
    partitionType: Optional[PartitionType]
    percentUsed: Optional[int]
    fileVault2State: Optional[ComputerPartitionFileVault2State]
    fileVault2ProgressPercent: Optional[int]
    lvmManaged: Optional[bool]


class ComputerDisk(BaseModel, extra=Extra.allow):
    id: Optional[str]
    device: Optional[str]
    model: Optional[str]
    revision: Optional[str]
    serialNumber: Optional[str]
    sizeMegabytes: Optional[int]
    smartStatus: Optional[str]
    type: Optional[str]
    partitions: Optional[List[ComputerPartition]] = None


class ComputerStorage(BaseModel, extra=Extra.allow):
    bootDriveAvailableSpaceMegabytes: Optional[int]
    disks: Optional[List[ComputerDisk]]


# Computer User and Location Model


class ComputerUserAndLocation(BaseModel, extra=Extra.allow):
    username: Optional[str]
    realname: Optional[str]
    email: Optional[str]
    position: Optional[str]
    phone: Optional[str]
    departmentId: Optional[str]
    buildingId: Optional[str]
    room: Optional[str]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]


# Computer Configuration Profile Model


class ComputerConfigurationProfile(BaseModel, extra=Extra.allow):
    id: Optional[str]
    username: Optional[str]
    lastInstalled: Optional[datetime]
    removable: Optional[bool]
    displayName: Optional[str]
    profileIdentifier: Optional[str]


# Computer Printer Model


class ComputerPrinter(BaseModel, extra=Extra.allow):
    name: Optional[str]
    type: Optional[str]
    uri: Optional[str]
    location: Optional[str]


# Computer Service Model


class ComputerService(BaseModel, extra=Extra.allow):
    name: Optional[str]


# Computer Hardware Models


class ComputerHardware(BaseModel, extra=Extra.allow):
    make: Optional[str]
    model: Optional[str]
    modelIdentifier: Optional[str]
    serialNumber: Optional[str]
    processorSpeedMhz: Optional[int]
    processorCount: Optional[int]
    coreCount: Optional[int]
    processorType: Optional[str]
    processorArchitecture: Optional[str]
    busSpeedMhz: Optional[int]
    cacheSizeKilobytes: Optional[int]
    networkAdapterType: Optional[str]
    macAddress: Optional[str]
    altNetworkAdapterType: Optional[str]
    altMacAddress: Optional[str]
    totalRamMegabytes: Optional[int]
    openRamSlots: Optional[int]
    batteryCapacityPercent: Optional[int]
    smcVersion: Optional[str]
    nicSpeed: Optional[str]
    opticalDrive: Optional[str]
    bootRom: Optional[str]
    bleCapable: Optional[bool]
    supportsIosAppInstalls: Optional[bool]
    appleSilicon: Optional[bool]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]


# Computer Local User Account Models


class UserAccountType(str, Enum):
    LOCAL: str = "LOCAL"
    MOBILE: str = "MOBILE"
    UNKNOWN: str = "UNKNOWN"


class AzureActiveDirectoryId(str, Enum):
    ACTIVATED: str = "ACTIVATED"
    DEACTIVATED: str = "DEACTIVATED"
    UNRESPONSIVE: str = "UNRESPONSIVE"
    UNKNOWN: str = "UNKNOWN"


class ComputerLocalUserAccount(BaseModel, extra=Extra.allow):
    uid: Optional[str]
    username: Optional[str]
    fullName: Optional[str]
    admin: Optional[bool]
    homeDirectory: Optional[str]
    homeDirectorySizeMb: Optional[int]
    fileVault2Enabled: Optional[bool]
    userAccountType: Optional[UserAccountType]
    passwordMinLength: Optional[int]
    passwordMaxAge: Optional[int]
    passwordMinComplexCharacters: Optional[int]
    passwordHistoryDepth: Optional[int]
    passwordRequireAlphanumeric: Optional[bool]
    computerAzureActiveDirectoryId: Optional[str]
    userAzureActiveDirectoryId: Optional[str]
    azureActiveDirectoryId: Optional[AzureActiveDirectoryId]


# Computer Certificate Models


class LifecycleStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"


class CertificateStatus(str, Enum):
    EXPIRING: str = "EXPIRING"
    EXPIRED: str = "EXPIRED"
    REVOKED: str = "REVOKED"
    PENDING_REVOKE: str = "PENDING_REVOKE"
    ISSUED: str = "ISSUED"


class ComputerCertificate(BaseModel, extra=Extra.allow):
    commonName: Optional[str]
    identity: Optional[bool]
    expirationDate: Optional[datetime]
    username: Optional[str]
    lifecycleStatus: Optional[LifecycleStatus]
    certificateStatus: Optional[CertificateStatus]
    subjectName: Optional[str]
    serialNumber: Optional[str]
    sha1Fingerprint: Optional[str]
    issuedDate: Optional[str]


# Computer Attachment Model


class ComputerAttachment(BaseModel, extra=Extra.allow):
    id: Optional[str]
    name: Optional[str]
    fileType: Optional[str]
    sizeBytes: Optional[int]


# Computer Plugin Model


class ComputerPlugin(BaseModel, extra=Extra.allow):
    name: Optional[str]
    version: Optional[str]
    path: Optional[str]


# Computer Package Receipt Model


class ComputerPackageReceipts(BaseModel, extra=Extra.allow):
    installedByJamfPro: Optional[List[str]]
    installedByInstallerSwu: Optional[List[str]]
    cached: Optional[List[str]]


# Computer Font Model


class ComputerFont(BaseModel, extra=Extra.allow):
    name: Optional[str]
    version: Optional[str]
    path: Optional[str]


# Computer Security Models


class SipStatus(str, Enum):
    NOT_COLLECTED: str = "NOT_COLLECTED"
    NOT_AVAILABLE: str = "NOT_AVAILABLE"
    DISABLED: str = "DISABLED"
    ENABLED: str = "ENABLED"


class GatekeeperStatus(str, Enum):
    NOT_COLLECTED: str = "NOT_COLLECTED"
    DISABLED: str = "DISABLED"
    APP_STORE_AND_IDENTIFIED_DEVELOPERS: str = "APP_STORE_AND_IDENTIFIED_DEVELOPERS"
    APP_STORE: str = "APP_STORE"


class SecureBootLevel(str, Enum):
    NO_SECURITY: str = "NO_SECURITY"
    MEDIUM_SECURITY: str = "MEDIUM_SECURITY"
    FULL_SECURITY: str = "FULL_SECURITY"
    NOT_SUPPORTED: str = "NOT_SUPPORTED"
    UNKNOWN: str = "UNKNOWN"


class ExternalBootLevel(str, Enum):
    ALLOW_BOOTING_FROM_EXTERNAL_MEDIA: str = "ALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA: str = "DISALLOW_BOOTING_FROM_EXTERNAL_MEDIA"
    NOT_SUPPORTED: str = "NOT_SUPPORTED"
    UNKNOWN: str = "UNKNOWN"


class ComputerSecurity(BaseModel, extra=Extra.allow):
    sipStatus: Optional[SipStatus]
    gatekeeperStatus: Optional[GatekeeperStatus]
    xprotectVersion: Optional[str]
    autoLoginDisabled: Optional[bool]
    remoteDesktopEnabled: Optional[bool]
    activationLockEnabled: Optional[bool]
    recoveryLockEnabled: Optional[bool]
    firewallEnabled: Optional[bool]
    secureBootLevel: Optional[SecureBootLevel]
    externalBootLevel: Optional[ExternalBootLevel]
    bootstrapTokenAllowed: Optional[bool]


# Computer Operating System Models


class FileVault2Status(str, Enum):
    NOT_APPLICABLE: str = "NOT_APPLICABLE"
    NOT_ENCRYPTED: str = "NOT_ENCRYPTED"
    BOOT_ENCRYPTED: str = "BOOT_ENCRYPTED"
    SOME_ENCRYPTED: str = "SOME_ENCRYPTED"
    ALL_ENCRYPTED: str = "ALL_ENCRYPTED"


class ComputerOperatingSystem(BaseModel, extra=Extra.allow):
    name: Optional[str]
    version: Optional[str]
    build: Optional[str]
    activeDirectoryStatus: Optional[str]
    fileVault2Status: Optional[FileVault2Status]
    softwareUpdateDeviceId: Optional[str]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]


# Computer Licensed Software Model


class ComputerLicensedSoftware(BaseModel, extra=Extra.allow):
    id: Optional[str]
    name: Optional[str]


# Computer iBeacon Model


class ComputeriBeacon(BaseModel, extra=Extra.allow):
    name: Optional[str]


# Computer Software Update Model


class ComputerSoftwareUpdate(BaseModel, extra=Extra.allow):
    name: Optional[str]
    version: Optional[str]
    packageName: Optional[str]


# Computer Content Caching Models


class ComputerContentCachingParentAlert(BaseModel, extra=Extra.allow):
    contentCachingParentAlertId: Optional[str]
    addresses: Optional[List[str]]
    className: Optional[str]
    postDate: Optional[datetime]


class ComputerContentCachingParentCapabilities(BaseModel, extra=Extra.allow):
    contentCachingParentCapabilitiesId: Optional[str]
    imports: Optional[bool]
    namespaces: Optional[bool]
    personalContent: Optional[bool]
    queryParameters: Optional[bool]
    sharedContent: Optional[bool]
    prioritization: Optional[bool]


class ComputerContentCachingParentLocalNetwork(BaseModel, extra=Extra.allow):
    contentCachingParentLocalNetworkId: Optional[str]
    speed: Optional[int]
    wired: Optional[bool]


class ComputerContentCachingParentDetails(BaseModel, extra=Extra.allow):
    contentCachingParentDetailsId: Optional[str]
    acPower: Optional[bool]
    cacheSizeBytes: Optional[int]
    capabilities: Optional[ComputerContentCachingParentCapabilities]
    portable: Optional[bool]
    localNetwork: Optional[List[ComputerContentCachingParentLocalNetwork]]


class ComputerContentCachingParent(BaseModel, extra=Extra.allow):
    contentCachingParentId: Optional[str]
    address: Optional[str]
    alerts: Optional[ComputerContentCachingParentAlert]
    details: Optional[ComputerContentCachingParentDetails]
    guid: Optional[str]
    healthy: Optional[bool]
    port: Optional[int]
    version: Optional[str]


class ComputerContentCachingAlert(BaseModel, extra=Extra.allow):
    cacheBytesLimit: Optional[int]
    className: Optional[str]
    pathPreventingAccess: Optional[str]
    postDate: Optional[datetime]
    reservedVolumeBytes: Optional[int]
    resource: Optional[str]


class ComputerContentCachingCacheDetail(BaseModel, extra=Extra.allow):
    computerContentCachingCacheDetailsId: Optional[str]
    categoryName: Optional[str]
    diskSpaceBytesUsed: Optional[int]


class ComputerContentCachingDataMigrationErrorUserInfo(BaseModel, extra=Extra.allow):
    key: Optional[str]
    value: Optional[str]


class ComputerContentCachingDataMigrationError(BaseModel, extra=Extra.allow):
    code: Optional[int]
    domain: Optional[str]
    userInfo: Optional[List[ComputerContentCachingDataMigrationErrorUserInfo]]


class ComputerContentCachingRegistrationStatus(str, Enum):
    CONTENT_CACHING_FAILED: str = "CONTENT_CACHING_FAILED"
    CONTENT_CACHING_PENDING: str = "CONTENT_CACHING_PENDING"
    CONTENT_CACHING_SUCCEEDED: str = "CONTENT_CACHING_SUCCEEDED"


class ComputerContentCachingTetheratorStatus(str, Enum):
    CONTENT_CACHING_UNKNOWN: str = "CONTENT_CACHING_UNKNOWN"
    CONTENT_CACHING_DISABLED: str = "CONTENT_CACHING_DISABLED"
    CONTENT_CACHING_ENABLED: str = "CONTENT_CACHING_ENABLED"


class ComputerContentCaching(BaseModel, extra=Extra.allow):
    computerContentCachingInformationId: Optional[str]
    parents: Optional[List[ComputerContentCachingParent]]
    alerts: Optional[List[ComputerContentCachingAlert]]
    activated: Optional[bool]
    active: Optional[bool]
    actualCacheBytesUsed: Optional[int]
    cacheDetails: Optional[List[ComputerContentCachingCacheDetail]]
    cacheBytesFree: Optional[int]
    cacheBytesLimit: Optional[int]
    cacheStatus: Optional[str]
    cacheBytesUsed: Optional[int]
    dataMigrationCompleted: Optional[bool]
    dataMigrationProgressPercentage: Optional[int]
    dataMigrationError: Optional[ComputerContentCachingDataMigrationError]
    maxCachePressureLast1HourPercentage: Optional[int]
    personalCacheBytesFree: Optional[int]
    personalCacheBytesLimit: Optional[int]
    personalCacheBytesUsed: Optional[int]
    port: Optional[int]
    publicAddress: Optional[str]
    registrationError: Optional[str]
    registrationResponseCode: Optional[int]
    registrationStarted: Optional[datetime]
    registrationStatus: Optional[ComputerContentCachingRegistrationStatus]
    restrictedMedia: Optional[bool]
    serverGuid: Optional[str]
    startupStatus: Optional[str]
    tetheratorStatus: Optional[ComputerContentCachingTetheratorStatus]
    totalBytesAreSince: Optional[datetime]
    totalBytesDropped: Optional[int]
    totalBytesImported: Optional[int]
    totalBytesReturnedToChildren: Optional[int]
    totalBytesReturnedToClients: Optional[int]
    totalBytesReturnedToPeers: Optional[int]
    totalBytesStoredFromOrigin: Optional[int]
    totalBytesStoredFromParents: Optional[int]
    totalBytesStoredFromPeers: Optional[int]


# Computer Group Membership Model


class ComputerGroupMembership(BaseModel, extra=Extra.allow):
    groupId: Optional[str]
    groupName: Optional[str]
    smartGroup: Optional[bool]


# Computer Inventory Model


class Computer(BaseModel, extra=Extra.allow):
    """Represents a full computer inventory record."""

    id: Optional[str]
    udid: Optional[str]
    general: Optional[ComputerGeneral] = Field(default_factory=ComputerGeneral)
    diskEncryption: Optional[ComputerDiskEncryption]
    purchasing: Optional[ComputerPurchase]
    applications: Optional[List[ComputerApplication]]
    storage: Optional[ComputerStorage]
    userAndLocation: Optional[ComputerUserAndLocation] = Field(
        default_factory=ComputerUserAndLocation
    )
    configurationProfiles: Optional[List[ComputerConfigurationProfile]]
    printers: Optional[List[ComputerPrinter]]
    services: Optional[List[ComputerService]]
    hardware: Optional[ComputerHardware]
    localUserAccounts: Optional[List[ComputerLocalUserAccount]]
    certificates: Optional[List[ComputerCertificate]]
    attachments: Optional[List[ComputerAttachment]]
    plugins: Optional[List[ComputerPlugin]]
    packageReceipts: Optional[ComputerPackageReceipts]
    fonts: Optional[List[ComputerFont]]
    security: Optional[ComputerSecurity]
    operatingSystem: Optional[ComputerOperatingSystem]
    licensedSoftware: Optional[List[ComputerLicensedSoftware]]
    ibeacons: Optional[List[ComputeriBeacon]]
    softwareUpdates: Optional[List[ComputerSoftwareUpdate]]
    extensionAttributes: Optional[List[ComputerExtensionAttribute]]
    contentCaching: Optional[ComputerContentCaching]
    groupMemberships: Optional[List[ComputerGroupMembership]]
