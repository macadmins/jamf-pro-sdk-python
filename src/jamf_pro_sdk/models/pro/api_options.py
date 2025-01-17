get_computer_inventory_v1_allowed_sections = [
    "ALL",
    "GENERAL",
    "DISK_ENCRYPTION",
    "PURCHASING",
    "APPLICATIONS",
    "STORAGE",
    "USER_AND_LOCATION",
    "CONFIGURATION_PROFILES",
    "PRINTERS",
    "SERVICES",
    "HARDWARE",
    "LOCAL_USER_ACCOUNTS",
    "CERTIFICATES",
    "ATTACHMENTS",
    "PLUGINS",
    "PACKAGE_RECEIPTS",
    "FONTS",
    "SECURITY",
    "OPERATING_SYSTEM",
    "LICENSED_SOFTWARE",
    "IBEACONS",
    "SOFTWARE_UPDATES",
    "EXTENSION_ATTRIBUTES",
    "CONTENT_CACHING",
    "GROUP_MEMBERSHIPS",
]

get_computer_inventory_v1_allowed_sort_fields = [
    "general.name",
    "udid",
    "id",
    "general.assetTag",
    "general.jamfBinaryVersion",
    "general.lastContactTime",
    "general.lastEnrolledDate",
    "general.lastCloudBackupDate",
    "general.reportDate",
    "general.remoteManagement.managementUsername",
    "general.mdmCertificateExpiration",
    "general.platform",
    "hardware.make",
    "hardware.model",
    "operatingSystem.build",
    "operatingSystem.supplementalBuildVersion",
    "operatingSystem.rapidSecurityResponse",
    "operatingSystem.name",
    "operatingSystem.version",
    "userAndLocation.realname",
    "purchasing.lifeExpectancy",
    "purchasing.warrantyDate",
]

get_computer_inventory_v1_allowed_filter_fields = [
    "general.name",
    "udid",
    "id",
    "general.assetTag",
    "general.barcode1",
    "general.barcode2",
    "general.enrolledViaAutomatedDeviceEnrollment",
    "general.lastIpAddress",
    "general.itunesStoreAccountActive",
    "general.jamfBinaryVersion",
    "general.lastContactTime",
    "general.lastEnrolledDate",
    "general.lastCloudBackupDate",
    "general.reportDate",
    "general.lastReportedIp",
    "general.managementId",
    "general.remoteManagement.managed",
    "general.mdmCapable.capable",
    "general.mdmCertificateExpiration",
    "general.platform",
    "general.supervised",
    "general.userApprovedMdm",
    "general.declarativeDeviceManagementEnabled",
    "hardware.bleCapable",
    "hardware.macAddress",
    "hardware.make",
    "hardware.model",
    "hardware.modelIdentifier",
    "hardware.serialNumber",
    "hardware.supportsIosAppInstalls",
    "hardware.appleSilicon",
    "operatingSystem.activeDirectoryStatus",
    "operatingSystem.fileVault2Status",
    "operatingSystem.build",
    "operatingSystem.supplementalBuildVersion",
    "operatingSystem.rapidSecurityResponse",
    "operatingSystem.name",
    "operatingSystem.version",
    "security.activationLockEnabled",
    "security.recoveryLockEnabled",
    "security.firewallEnabled",
    "serAndLocation.buildingId",
    "userAndLocation.departmentId",
    "userAndLocation.email",
    "userAndLocation.realname",
    "userAndLocation.phone",
    "userAndLocation.position",
    "userAndLocation.room",
    "userAndLocation.username",
    "diskEncryption.fileVault2Enabled",
    "purchasing.appleCareId",
    "purchasing.lifeExpectancy",
    "purchasing.purchased",
    "purchasing.leased",
    "purchasing.vendor",
    "purchasing.warrantyDate",
]

get_packages_v1_allowed_sort_fields = [
    "id",
    "packageName",
    "fileName",
    "categoryId",
    "info",
    "notes",
    "manifestFileName",
]

get_packages_v1_allowed_filter_fields = [
    "id",
    "packageName",
    "fileName",
    "categoryId",
    "info",
    "notes",
    "manifestFileName",
]

get_mdm_commands_v2_allowed_sort_fields = [
    "uuid",
    "clientManagementId",
    "command",
    "status",
    # "clientType",  # 500 error
    "dateSent",
    "validAfter",
    "dateCompleted",
    "profileIdentifier",
    "active",
]

get_mdm_commands_v2_allowed_filter_fields = [
    "uuid",
    "clientManagementId",
    "command",
    "status",
    "clientType",
    "dateSent",
    "validAfter",
    "dateCompleted",
    "profileId",  # profileIdentifier
    "active",
]

get_mdm_commands_v2_allowed_command_types = [
    "DEVICE_LOCATION",
    "ENABLE_LOST_MODE",
    "ACTIVATION_LOCK_BYPASS_CODE",
    "CLEAR_ACTIVATION_LOCK_BYPASS_CODE",
    "ACCOUNT_CONFIGURATION",
    "REFRESH_CELLULAR_PLANS",
    "SETTINGS",
    "CONTENT_CACHING_INFORMATION",
    "UNMANAGE_DEVICE",
    "ERASE_DEVICE",
    "DEVICE_LOCK",
    "CLEAR_PASSCODE",
    "DELETE_USER",
    "DEVICE_INFORMATION",
    "SHUT_DOWN_DEVICE",
    "RESTART_DEVICE",
    "INSTALL_BYO_PROFILE",
    "REMOVE_PROFILE",
    "INSTALL_PROFILE",
    "REINSTALL_PROFILE",
    "INSTALL_PROVISIONING_PROFILE",
    "PROFILE_LIST",
    "REMOVE_PROVISIONING_PROFILE",
    "CERTIFICATE_LIST",
    "INSTALLED_APPLICATION_LIST",
    "MANAGED_APPLICATION_LIST",
    "INSTALL_APPLICATION",
    "INSTALL_ENTERPRISE_APPLICATION",
    "INSTALL_PACKAGE",
    "REMOVE_APPLICATION",
    "MANAGED_MEDIA_LIST",
    "INSTALL_MEDIA",
    "REMOVE_MEDIA",
    "APPLY_REDEMPTION_CODE",
    "SETTINGS_ENABLE_PERSONAL_HOTSPOT",
    "SETTINGS_DISABLE_PERSONAL_HOTSPOT",
    "UPDATE_INVENTORY",
    "WALLPAPER",
    "DEVICE_CONFIGURED",
    "RESTRICTIONS",
    "ENABLE_REMOTE_DESKTOP",
    "DISABLE_REMOTE_DESKTOP",
    "SECURITY_INFO",
    "MARK_AS_UNMANAGED",
    "QUERY_RESPONSES",
    "AVAILABLE_OS_UPDATES",
    "PROVISIONING_PROFILE_LIST",
    "SCHEDULE_OS_UPDATE",
    "OS_UPDATE_STATUS",
    "INVITE_TO_PROGRAM",
    "PUSH_TRIGGER",
    "CLEAR_RESTRICTIONS_PASSWORD",
    "BLANK_PUSH",
    "CORPORATE_WIPE",
    "DEVICE_INFO_ACCOUNT_HASH",
    "DEVICE_INFO_ITUNES_ACTIVE",
    "DEVICE_INFO_LAST_CLOUD_BACKUP_DATE",
    "DEVICE_INFO_ACTIVE_MANAGED_USERS",
    "DEVICE_NAME",
    "ENABLE_ACTIVATION_LOCK",
    "DISABLE_ACTIVATION_LOCK",
    "LAST_CLOUD_BACKUP_DATE",
    "MARK_AS_CORPORATE_WIPE",
    "REQUEST_MIRRORING",
    "SETTINGS_DISABLE_DATA_ROAMING",
    "SETTINGS_DISABLE_VOICE_ROAMING",
    "SETTINGS_DISABLE_DIAGNOSTIC_SUBMISSION",
    "SETTINGS_DISABLE_APP_ANALYTICS",
    "SETTINGS_ENABLE_DATA_ROAMING",
    "SETTINGS_ENABLE_VOICE_ROAMING",
    "SETTINGS_ENABLE_DIAGNOSTIC_SUBMISSION",
    "SETTINGS_ENABLE_APP_ANALYTICS",
    "SETTINGS_ENABLE_BLUETOOTH",
    "SETTINGS_DISABLE_BLUETOOTH",
    "SETTINGS_MOBILE_DEVICE_PER_APP_VPN",
    "SETTINGS_MOBILE_DEVICE_APPLICATION_ATTRIBUTES",
    "STOP_MIRRORING",
    "PASSCODE_LOCK_GRACE_PERIOD",
    "SCHEDULE_OS_UPDATE_SCAN",
    "PLAY_LOST_MODE_SOUND",
    "DISABLE_LOST_MODE",
    "LOG_OUT_USER",
    "USER_LIST",
    "VALIDATE_APPLICATIONS",
    "UNLOCK_USER_ACCOUNT",
    "SET_RECOVERY_LOCK",
    "DECLARATIVE_MANAGEMENT",
    "SET_AUTO_ADMIN_PASSWORD",
    "UNKNOWN",
]

get_mobile_device_inventory_v2_allowed_sections = [
    "GENERAL",
    "HARDWARE",
    "USER_AND_LOCATION",
    "PURCHASING",
    "SECURITY",
    "APPLICATIONS",
    "EBOOKS",
    "NETWORK",
    "SERVICE_SUBSCRIPTIONS",
    "CERTIFICATES",
    "PROFILES",
    "USER_PROFILES",
    "PROVISIONING_PROFILES",
    "SHARED_USERS",
    "EXTENSION_ATTRIBUTES",
]

get_mobile_device_inventory_v2_allowed_sort_fields = [
    "airPlayPassword",
    "appAnalyticsEnabled",
    "assetTag",
    "availableSpaceMb",
    "batteryLevel",
    "batteryHealth",
    "bluetoothLowEnergyCapable",
    "bluetoothMacAddress",
    "capacityMb",
    "lostModeEnabledDate",
    "declarativeDeviceManagementEnabled",
    "deviceId",
    "deviceLocatorServiceEnabled",
    "devicePhoneNumber",
    "diagnosticAndUsageReportingEnabled",
    "displayName",
    "doNotDisturbEnabled",
    "enrollmentSessionTokenValid",
    "exchangeDeviceId",
    "cloudBackupEnabled",
    "osBuild",
    "osSupplementalBuildVersion",
    "osVersion",
    "osRapidSecurityResponse",
    "ipAddress",
    "itunesStoreAccountActive",
    "mobileDeviceId",
    "languages",
    "lastBackupDate",
    "lastEnrolledDate",
    "lastCloudBackupDate",
    "lastInventoryUpdateDate",
    "locales",
    "locationServicesForSelfServiceMobileEnabled",
    "lostModeEnabled",
    "managed",
    "mdmProfileExpirationDate",
    "model",
    "modelIdentifier",
    "modelNumber",
    "modemFirmwareVersion",
    "quotaSize",
    "residentUsers",
    "serialNumber",
    "sharedIpad",
    "supervised",
    "tethered",
    "timeZone",
    "udid",
    "usedSpacePercentage",
    "wifiMacAddress",
    "deviceOwnershipType",
    "building",
    "department",
    "emailAddress",
    "fullName",
    "userPhoneNumber",
    "position",
    "room",
    "username",
    "appleCareId",
    "leaseExpirationDate",
    "ifeExpectancyYears",
    "poDate",
    "poNumber",
    "purchasePrice",
    "purchasedOrLeased",
    "purchasingAccount",
    "purchasingContact",
    "vendor",
    "warrantyExpirationDate",
    "activationLockEnabled",
    "blockEncryptionCapable",
    "dataProtection",
    "fileEncryptionCapable",
    "hardwareEncryptionSupported",
    "jailbreakStatus",
    "passcodeCompliant",
    "passcodeCompliantWithProfile",
    "passcodeLockGracePeriodEnforcedSeconds",
    "passcodePresent",
    "personalDeviceProfileCurrent",
    "carrierSettingsVersion",
    "cellularTechnology",
    "currentCarrierNetwork",
    "currentMobileCountryCode",
    "currentMobileNetworkCode",
    "dataRoamingEnabled",
    "eid",
    "network",
    "homeMobileCountryCode",
    "homeMobileNetworkCode",
    "iccid",
    "imei",
    "imei2",
    "meid",
    "personalHotspotEnabled",
    "voiceRoamingEnabled",
    "roaming",
]

get_mobile_device_inventory_v2_allowed_filter_fields = [
    "airPlayPassword",
    "appAnalyticsEnabled",
    "assetTag",
    "availableSpaceMb",
    "batteryLevel",
    "bluetoothLowEnergyCapable",
    "bluetoothMacAddress",
    "capacityMb",
    "declarativeDeviceManagementEnabled",
    "deviceId",
    "deviceLocatorServiceEnabled",
    "devicePhoneNumber",
    "diagnosticAndUsageReportingEnabled",
    "displayName",
    "doNotDisturbEnabled",
    "exchangeDeviceId",
    "cloudBackupEnabled",
    "osBuild",
    "osSupplementalBuildVersion",
    "osVersion",
    "osRapidSecurityResponse",
    "ipAddress",
    "itunesStoreAccountActive",
    "mobileDeviceId",
    "languages",
    "locales",
    "locationServicesForSelfServiceMobileEnabled",
    "lostModeEnabled",
    "managed",
    "model",
    "modelIdentifier",
    "modelNumber",
    "modemFirmwareVersion",
    "quotaSize",
    "residentUsers",
    "serialNumber",
    "sharedIpad",
    "supervised",
    "tethered",
    "timeZone",
    "udid",
    "usedSpacePercentage",
    "wifiMacAddress",
    "building",
    "department",
    "emailAddress",
    "fullName",
    "userPhoneNumber",
    "position",
    "room",
    "username",
    "appleCareId",
    "lifeExpectancyYears",
    "poNumber",
    "purchasePrice",
    "purchasedOrLeased",
    "purchasingAccount",
    "purchasingContact",
    "vendor",
    "activationLockEnabled",
    "blockEncryptionCapable",
    "dataProtection",
    "fileEncryptionCapable",
    "passcodeCompliant",
    "passcodeCompliantWithProfile",
    "passcodeLockGracePeriodEnforcedSeconds",
    "passcodePresent",
    "personalDeviceProfileCurrent",
    "carrierSettingsVersion",
    "currentCarrierNetwork",
    "currentMobileCountryCode",
    "currentMobileNetworkCode",
    "dataRoamingEnabled",
    "eid",
    "network",
    "homeMobileCountryCode",
    "homeMobileNetworkCode",
    "iccid",
    "imei",
    "imei2",
    "meid",
    "personalHotspotEnabled",
    "roaming",
]
