from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import Extra, Field

from .. import BaseModel
from . import ClassicApiModel, ClassicDeviceLocation, ClassicDevicePurchasing, ClassicSite

_XML_ARRAY_ITEM_NAMES = {
    # Computer
    "certificates": "certificate",
    "extension_attributes": "extension_attribute",
    # Computer.Hardware
    "filevault2_users": "user",
    "storage": "device",
    "partitions": "partition",
    "mapped_printers": "printer",
    # Computer.Software
    "licensed_software": "name",
    "installed_by_casper": "package",
    "installed_by_installer_swu": "package",
    "cached_by_casper": "package",
    "available_software_updates": "name",
    "available_updates": "update",
    "running_services": "name",
    "applications": "application",
    "fonts": "font",
    "plugins": "plugin",
    # Computer.GroupsAccounts
    "computer_group_memberships": "group",
    "local_accounts": "user",
    # Computer.ConfigurationProfiles
    "configuration_profiles": "configuration_profile",
}

# Computer.General Models


class ClassicComputerGeneralRemoteManagement(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.general.remote_management

    - :class:`str` management_password: This attribute is only used in POST/PUT operations
    - :class:`str` management_password_sha256: This attribute is read-only
    """

    managed: Optional[bool]
    management_username: Optional[str]
    management_password: Optional[str]
    management_password_sha256: Optional[str]


class ClassicComputerGeneralMdmCapableUsers(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.general.mdm_capable_users"""

    mdm_capable_user: Optional[str]


class ClassicComputerGeneralManagementStatus(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.general.management_status"""

    enrolled_via_dep: Optional[bool]
    user_approved_enrollment: Optional[bool]
    user_approved_mdm: Optional[bool]


class ClassicComputerGeneral(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.general"""

    id: Optional[int]
    name: Optional[str]
    mac_address: Optional[str]
    network_adapter_type: Optional[str]
    alt_mac_address: Optional[str]
    alt_network_adapter_type: Optional[str]
    ip_address: Optional[str]
    last_reported_ip: Optional[str]
    serial_number: Optional[str]
    udid: Optional[str]
    jamf_version: Optional[str]
    platform: Optional[str]
    barcode_1: Optional[str]
    barcode_2: Optional[str]
    asset_tag: Optional[str]
    remote_management: Optional[ClassicComputerGeneralRemoteManagement]
    supervised: Optional[bool]
    mdm_capable: Optional[bool]
    mdm_capable_users: Optional[Union[dict, ClassicComputerGeneralMdmCapableUsers]]
    management_status: Optional[ClassicComputerGeneralManagementStatus]
    report_date: Optional[str]
    report_date_epoch: Optional[int]
    report_date_utc: Union[Optional[datetime], Optional[str]]
    last_contact_time: Optional[str]
    last_contact_time_epoch: Optional[int]
    last_contact_time_utc: Optional[str]
    initial_entry_date: Optional[str]
    initial_entry_date_epoch: Optional[int]
    initial_entry_date_utc: Union[Optional[datetime], Optional[str]]
    last_cloud_backup_date_epoch: Optional[int]
    last_cloud_backup_date_utc: Union[Optional[datetime], Optional[str]]
    last_enrolled_date_epoch: Optional[int]
    last_enrolled_date_utc: Union[Optional[datetime], Optional[str]]
    mdm_profile_expiration_epoch: Optional[int]
    mdm_profile_expiration_utc: Union[Optional[datetime], Optional[str]]
    distribution_point: Optional[str]
    sus: Optional[str]
    site: Optional[ClassicSite]
    itunes_store_account_is_active: Optional[bool]


# Computer.Hardware Models


class ClassicComputerHardwareStorageDevicePartition(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.hardware.storage.partitions"""

    name: Optional[str]
    size: Optional[int]
    type: Optional[str]
    partition_capacity_mb: Optional[int]
    percentage_full: Optional[int]
    available_mb: Optional[int]
    filevault_status: Optional[str]
    filevault_percent: Optional[int]
    filevault2_status: Optional[str]
    filevault2_percent: Optional[int]
    boot_drive_available_mb: Optional[int]
    lvgUUID: Optional[str]
    lvUUID: Optional[str]
    pvUUID: Optional[str]


class ClassicComputerHardwareStorageDevice(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.hardware.storage"""

    disk: Optional[str]
    model: Optional[str]
    revision: Optional[str]
    serial_number: Optional[str]
    size: Optional[int]
    drive_capacity_mb: Optional[int]
    connection_type: Optional[str]
    smart_status: Optional[str]
    partitions: Optional[List[ClassicComputerHardwareStorageDevicePartition]]


class ClassicComputerHardwareMappedPrinter(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.hardware.mapped_printers"""

    name: Optional[str]
    uri: Optional[str]
    type: Optional[str]
    location: Optional[str]


class ClassicComputerHardware(ClassicApiModel):
    """Computer nested model: computer.hardware"""

    _xml_root_name = "hardware"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    make: Optional[str]
    model: Optional[str]
    model_identifier: Optional[str]
    os_name: Optional[str]
    os_version: Optional[str]
    os_build: Optional[str]
    software_update_device_id: Optional[str]
    active_directory_status: Optional[str]
    service_pack: Optional[str]
    processor_type: Optional[str]
    is_apple_silicon: Optional[bool]
    processor_architecture: Optional[str]
    processor_speed: Optional[int]
    processor_speed_mhz: Optional[int]
    number_processors: Optional[int]
    number_cores: Optional[int]
    total_ram: Optional[int]
    total_ram_mb: Optional[int]
    boot_rom: Optional[str]
    bus_speed: Optional[int]
    bus_speed_mhz: Optional[int]
    battery_capacity: Optional[int]
    cache_size: Optional[int]
    cache_size_kb: Optional[int]
    available_ram_slots: Optional[int]
    optical_drive: Optional[str]
    nic_speed: Optional[str]
    smc_version: Optional[str]
    ble_capable: Optional[bool]
    supports_ios_app_installs: Optional[bool]
    sip_status: Optional[str]
    gatekeeper_status: Optional[str]
    xprotect_version: Optional[str]
    institutional_recovery_key: Optional[str]
    disk_encryption_configuration: Optional[str]
    filevault2_users: Optional[List[str]]
    storage: Optional[List[ClassicComputerHardwareStorageDevice]]
    mapped_printers: Optional[List[ClassicComputerHardwareMappedPrinter]]


# Computer.Certificate Models


class ClassicComputerCertificate(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.certificates"""

    common_name: Optional[str]
    identity: Optional[bool]
    expires_utc: Optional[str]
    expires_epoch: Optional[int]
    name: Optional[str]


# Computer.Security Models


class ClassicComputerSecurity(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.security"""

    activation_lock: Optional[bool]
    recovery_lock_enabled: Optional[bool]
    secure_boot_level: Optional[str]
    external_boot_level: Optional[str]
    firewall_enabled: Optional[bool]


# Computer.Software Models


class ClassicComputerSoftwareAvailableUpdate(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.software.available_updates"""

    name: Optional[str]
    package_name: Optional[str]
    version: Optional[str]


class ClassicComputerSoftwareItem(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.software.applications, computer.software.fonts,
    computer.software.plugins
    """

    name: Optional[str]
    path: Optional[str]
    version: Optional[str]
    bundle_id: Optional[str]


class ClassicComputerSoftware(BaseModel, extra=Extra.allow):  # Lots of assumptions in this object
    """Computer nested model: computer.software"""

    unix_executables: Optional[List[str]]
    licensed_software: Optional[List[str]]
    installed_by_casper: Optional[List[str]]
    installed_by_installer_swu: Optional[List[str]]
    cached_by_casper: Optional[List[str]]
    available_software_updates: Optional[List[str]]
    available_updates: Union[Optional[List[ClassicComputerSoftwareAvailableUpdate]], Optional[dict]]
    running_services: Optional[List[str]]
    applications: Optional[List[ClassicComputerSoftwareItem]]
    fonts: Optional[List[ClassicComputerSoftwareItem]]
    plugins: Optional[List[ClassicComputerSoftwareItem]]


# Computer.ExtensionAttributes Models


class ClassicComputerExtensionAttribute(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.extension_attributes"""

    id: Optional[int]
    name: Optional[str]
    type: Optional[str]
    multi_value: Optional[bool]
    value: Optional[str]


# Computer GroupsAccounts Models


class ClassicComputerGroupsAccountsLocalAccount(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.groups_accounts.local_accounts"""

    name: Optional[str]
    realname: Optional[str]
    uid: Optional[str]
    home: Optional[str]
    home_size: Optional[str]
    home_size_mb: Optional[int]
    administrator: Optional[bool]
    filevault_enabled: Optional[bool]


class ClassicComputerGroupsAccountsUserInventoriesUser(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.groups_accounts.user_inventories.user"""

    username: Optional[str]
    password_history_depth: Optional[str]
    password_min_length: Optional[str]
    password_max_age: Optional[str]
    password_min_complex_characters: Optional[str]
    password_require_alphanumeric: Optional[str]


class ClassicComputerGroupsAccountsUserInventories(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.groups_accounts.user_inventories

    There is a bug with this API resource!

    XML response::

        <user_inventories>
          <disable_automatic_login>true</disable_automatic_login>
          <user>...</user>
          <user>...</user>
        </user_inventories>

    JSON response::

        {
            "user_inventories": {
                "disable_automatic_login": true,
                "user": {...}
            }
        }

    Only one user is represented in a JSON response
    TODO: Accurate data can only be obtained using an XML response
    """

    disable_automatic_login: Optional[bool]
    user: Union[
        Optional[ClassicComputerGroupsAccountsUserInventoriesUser],
        Optional[List[ClassicComputerGroupsAccountsUserInventoriesUser]],
    ]


class ClassicComputerGroupsAccounts(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.groups_accounts"""

    computer_group_memberships: Optional[List[str]]
    local_accounts: Optional[List[ClassicComputerGroupsAccountsLocalAccount]]
    user_inventories: Optional[ClassicComputerGroupsAccountsUserInventories]


# Computer.ConfigurationProfiles Models


class ClassicComputerConfigurationProfile(BaseModel, extra=Extra.allow):
    """Computer nested model: computer.configuration_profiles"""

    id: Optional[int]
    name: Optional[str]
    uuid: Optional[str]
    is_removable: Optional[bool]


# Computer Models


class ClassicComputersItem(BaseModel, extra=Extra.allow):
    """Represents a computer record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_computers` operation.

    Unless the ``basic`` subset has been requested, only ``id`` and ``name`` will be
    populated.
    """

    id: int
    name: str
    managed: Optional[bool]
    username: Optional[str]
    model: Optional[str]
    department: Optional[str]
    building: Optional[str]
    mac_address: Optional[str]
    udid: Optional[str]
    serial_number: Optional[str]
    report_date_utc: Union[Optional[datetime], Optional[str]]
    report_date_epoch: Optional[int]


class ClassicComputer(ClassicApiModel):
    """Represents a full computer inventory record.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``general``, ``location``, and ``extension_attributes``. To bypass this
    behavior export the model using
    :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    _xml_root_name = "computer"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"general", "location", "extension_attributes"}

    general: Optional[ClassicComputerGeneral] = Field(default_factory=ClassicComputerGeneral)
    location: Optional[ClassicDeviceLocation] = Field(default_factory=ClassicDeviceLocation)
    purchasing: Optional[ClassicDevicePurchasing]
    # Peripherals are a deprecated feature of Jamf Pro
    peripherals: Optional[Any]
    hardware: Optional[ClassicComputerHardware]
    certificates: Optional[List[ClassicComputerCertificate]]
    security: Optional[ClassicComputerSecurity]
    software: Optional[ClassicComputerSoftware]
    extension_attributes: Optional[List[ClassicComputerExtensionAttribute]] = Field(
        default_factory=list
    )
    groups_accounts: Optional[ClassicComputerGroupsAccounts]
    # iPhones in Computer inventory is a deprecated feature of Jamf Pro
    iphones: Optional[Any]
    configuration_profiles: Optional[List[ClassicComputerConfigurationProfile]]
