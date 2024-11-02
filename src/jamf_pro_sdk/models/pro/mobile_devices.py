from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import ConfigDict

from .. import BaseModel


class MobileDeviceType(str, Enum):
    """Not in use: the value of this attribute can be an undocumented state."""

    iOS = "iOS"
    tvOS = "tvOS"


class MobileDeviceExtensionAttributeType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DATE = "DATE"


class MobileDeviceExtensionAttribute(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[MobileDeviceExtensionAttributeType] = None
    value: Optional[List[str]] = None
    extensionAttributeCollectionAllowed: Optional[bool] = None
    inventoryDisplay: Optional[str] = None


class MobileDeviceHardware(BaseModel):
    model_config = ConfigDict(extra="allow")

    capacityMb: Optional[int] = None
    availableSpaceMb: Optional[int] = None
    usedSpacePercentage: Optional[int] = None
    batteryLevel: Optional[int] = None
    serialNumber: Optional[str] = None
    wifiMacAddress: Optional[str] = None
    bluetoothMacAddress: Optional[str] = None
    modemFirmwareVersion: Optional[str] = None
    model: Optional[str] = None
    modelIdentifier: Optional[str] = None
    modelNumber: Optional[str] = None
    bluetoothLowEnergyCapable: Optional[bool] = None
    deviceId: Optional[str] = None
    extensionAttributes: Optional[List[MobileDeviceExtensionAttribute]] = None


class MobileDeviceUserAndLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    username: Optional[str] = None
    realName: Optional[str] = None
    emailAddress: Optional[str] = None
    position: Optional[str] = None
    phoneNumber: Optional[str] = None
    departmentId: Optional[str] = None
    buildingId: Optional[str] = None
    room: Optional[str] = None
    building: Optional[str] = None
    department: Optional[str] = None
    extensionAttributes: Optional[List[MobileDeviceExtensionAttribute]] = None


class MobileDevicePurchasing(BaseModel):
    model_config = ConfigDict(extra="allow")

    purchased: Optional[bool] = None
    leased: Optional[bool] = None
    poNumber: Optional[str] = None
    vendor: Optional[str] = None
    appleCareId: Optional[str] = None
    purchasePrice: Optional[str] = None
    purchasingAccount: Optional[str] = None
    poDate: Optional[datetime] = None
    warrantyExpiresDate: Optional[datetime] = None
    leaseExpiresDate: Optional[datetime] = None
    lifeExpectancy: Optional[int] = None
    purchasingContact: Optional[str] = None
    extensionAttributes: Optional[List[MobileDeviceExtensionAttribute]] = None


class MobileDeviceApplication(BaseModel):
    model_config = ConfigDict(extra="allow")

    identifier: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    shortVersion: Optional[str] = None
    managementStatus: Optional[str] = None
    validationStatus: Optional[bool] = None
    bundleSize: Optional[str] = None
    dynamicSize: Optional[str] = None


class MobileDeviceCertificate(BaseModel):
    model_config = ConfigDict(extra="allow")

    commonName: Optional[str] = None
    identity: Optional[bool] = None
    expirationDate: Optional[datetime] = None


class MobileDeviceProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    displayName: Optional[str] = None
    version: Optional[str] = None
    uuid: Optional[str] = None
    identifier: Optional[str] = None
    removable: Optional[bool] = None
    lastInstalled: Optional[datetime] = None


class MobileDeviceUserProfile(MobileDeviceProfile):
    """Extends :class:`~jamf_pro_sdk.models.pro.mobile_devices.MobileDeviceProfile`."""

    model_config = ConfigDict(extra="allow")

    username: Optional[str] = None


class MobileDeviceOwnershipType(str, Enum):
    Institutional = "Institutional"
    PersonalDeviceProfile = "PersonalDeviceProfile"
    UserEnrollment = "UserEnrollment"
    AccountDrivenUserEnrollment = "AccountDrivenUserEnrollment"
    AccountDrivenDeviceEnrollment = "AccountDrivenDeviceEnrollment"


class MobileDeviceEnrollmentMethodPrestage(BaseModel):
    model_config = ConfigDict(extra="allow")

    mobileDevicePrestageId: Optional[str] = None
    profileName: Optional[str] = None


class MobileDeviceGeneral(BaseModel):
    model_config = ConfigDict(extra="allow")

    udid: Optional[str] = None
    displayName: Optional[str] = None
    assetTag: Optional[str] = None
    siteId: Optional[str] = None
    lastInventoryUpdateDate: Optional[datetime] = None
    osVersion: Optional[str] = None
    osRapidSecurityResponse: Optional[str] = None
    osBuild: Optional[str] = None
    osSupplementalBuildVersion: Optional[str] = None
    softwareUpdateDeviceId: Optional[str] = None
    ipAddress: Optional[str] = None
    managed: Optional[bool] = None
    supervised: Optional[bool] = None
    deviceOwnershipType: Optional[MobileDeviceOwnershipType] = None
    enrollmentMethodPrestage: Optional[MobileDeviceEnrollmentMethodPrestage] = None
    enrollmentSessionTokenValid: Optional[bool] = None
    lastEnrolledDate: Optional[datetime] = None
    mdmProfileExpirationDate: Optional[datetime] = None
    timeZone: Optional[str] = None
    declarativeDeviceManagementEnabled: Optional[bool] = None
    extensionAttributes: Optional[List[MobileDeviceExtensionAttribute]] = None
    airPlayPassword: Optional[str] = None
    locales: Optional[str] = None
    languages: Optional[str] = None


class MobileDeviceSecurityLostModeLocation(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    lastLocationUpdate: Optional[datetime] = None
    lostModeLocationHorizontalAccuracyMeters: Optional[int] = None
    lostModeLocationVerticalAccuracyMeters: Optional[int] = None
    lostModeLocationAltitudeMeters: Optional[int] = None
    lostModeLocationSpeedMetersPerSecond: Optional[int] = None
    lostModeLocationCourseDegrees: Optional[int] = None
    lostModeLocationTimestamp: Optional[str] = None


class MobileDeviceSecurity(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    dataProtected: Optional[bool] = None
    blockLevelEncryptionCapable: Optional[bool] = None
    fileLevelEncryptionCapable: Optional[bool] = None
    passcodePresent: Optional[bool] = None
    passcodeCompliant: Optional[bool] = None
    passcodeCompliantWithProfile: Optional[bool] = None
    hardwareEncryption: Optional[int] = None
    activationLockEnabled: Optional[bool] = None
    jailBreakDetected: Optional[bool] = None
    passcodeLockGracePeriodEnforcedSeconds: Optional[int] = None
    personalDeviceProfileCurrent: Optional[bool] = None
    lostModeEnabled: Optional[bool] = None
    lostModePersistent: Optional[bool] = None
    lostModeMessage: Optional[str] = None
    lostModePhoneNumber: Optional[str] = None
    lostModeFootnote: Optional[str] = None
    lostModeLocation: Optional[MobileDeviceSecurityLostModeLocation] = None


class MobileDeviceEbook(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    author: Optional[str] = None
    title: Optional[str] = None
    version: Optional[str] = None
    kind: Optional[str] = None
    managementState: Optional[str] = None


class MobileDeviceNetwork(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    cellularTechnology: Optional[str] = None
    voiceRoamingEnabled: Optional[bool] = None
    imei: Optional[str] = None
    iccid: Optional[str] = None
    meid: Optional[str] = None
    eid: Optional[str] = None
    carrierSettingsVersion: Optional[str] = None
    currentCarrierNetwork: Optional[str] = None
    currentMobileCountryCode: Optional[str] = None
    currentMobileNetworkCode: Optional[str] = None
    homeCarrierNetwork: Optional[str] = None
    homeMobileCountryCode: Optional[str] = None
    homeMobileNetworkCode: Optional[str] = None
    dataRoamingEnabled: Optional[bool] = None
    roaming: Optional[bool] = None
    personalHotspotEnabled: Optional[bool] = None
    phoneNumber: Optional[str] = None


class MobileDeviceServiceSubscription(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    carrierSettingsVersion: Optional[str] = None
    currentCarrierNetwork: Optional[str] = None
    currentMobileCountryCode: Optional[str] = None
    currentMobileNetworkCode: Optional[str] = None
    subscriberCarrierNetwork: Optional[str] = None
    eid: Optional[str] = None
    iccid: Optional[str] = None
    imei: Optional[str] = None
    dataPreferred: Optional[bool] = None
    roaming: Optional[bool] = None
    voicePreferred: Optional[bool] = None
    label: Optional[str] = None
    labelId: Optional[str] = None
    meid: Optional[str] = None
    phoneNumber: Optional[str] = None
    slot: Optional[str] = None


class ProvisioningProfile(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    displayName: Optional[str] = None
    uuid: Optional[str] = None
    expirationDate: Optional[datetime] = None


class SharedUser(BaseModel):
    """iOS devices only."""

    model_config = ConfigDict(extra="allow")

    managedAppleId: Optional[str] = None
    loggedIn: Optional[bool] = None
    dataToSync: Optional[bool] = None


class MobileDevice(BaseModel):
    """Represents a full mobile device inventory record."""

    model_config = ConfigDict(extra="allow")

    mobileDeviceId: Optional[str] = None
    deviceType: Optional[str] = None
    hardware: Optional[MobileDeviceHardware] = None
    userAndLocation: Optional[MobileDeviceUserAndLocation] = None
    purchasing: Optional[MobileDevicePurchasing] = None
    applications: Optional[List[MobileDeviceApplication]] = None
    certificates: Optional[List[MobileDeviceCertificate]] = None
    profiles: Optional[List[MobileDeviceProfile]] = None
    userProfiles: Optional[List[MobileDeviceUserProfile]] = None
    extensionAttributes: Optional[List[MobileDeviceExtensionAttribute]] = None
    general: Optional[MobileDeviceGeneral] = None
    security: Optional[MobileDeviceSecurity] = None
    ebooks: Optional[List[MobileDeviceEbook]] = None
    network: Optional[MobileDeviceNetwork] = None
    serviceSubscriptions: Optional[List[MobileDeviceServiceSubscription]] = None
    provisioningProfiles: Optional[List[ProvisioningProfile]] = None
    sharedUsers: Optional[List[SharedUser]] = None
