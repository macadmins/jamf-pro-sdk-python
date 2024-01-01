from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import ConfigDict, Field

from .. import BaseModel
from . import (
    ClassicApiModel,
    ClassicDeviceLocation,
    ClassicDevicePurchasing,
    ClassicSite,
)

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


class ClassicComputerGeneralRemoteManagement(BaseModel):
    """Computer nested model: computer.general.remote_management

    - :class:`str` management_password: This attribute is only used in POST/PUT operations
    - :class:`str` management_password_sha256: This attribute is read-only
    """

    model_config = ConfigDict(extra="allow")

    managed: Optional[bool] = None
    management_username: Optional[str] = None
    management_password: Optional[str] = None
    management_password_sha256: Optional[str] = None


class ClassicComputerGeneralMdmCapableUsers(BaseModel):
    """Computer nested model: computer.general.mdm_capable_users"""

    model_config = ConfigDict(extra="allow")

    mdm_capable_user: Optional[str] = None


class ClassicComputerGeneralManagementStatus(BaseModel):
    """Computer nested model: computer.general.management_status"""

    model_config = ConfigDict(extra="allow")

    enrolled_via_dep: Optional[bool] = None
    user_approved_enrollment: Optional[bool] = None
    user_approved_mdm: Optional[bool] = None


class ClassicComputerGeneral(BaseModel):
    """Computer nested model: computer.general"""

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None
    mac_address: Optional[str] = None
    network_adapter_type: Optional[str] = None
    alt_mac_address: Optional[str] = None
    alt_network_adapter_type: Optional[str] = None
    ip_address: Optional[str] = None
    last_reported_ip: Optional[str] = None
    serial_number: Optional[str] = None
    udid: Optional[str] = None
    jamf_version: Optional[str] = None
    platform: Optional[str] = None
    barcode_1: Optional[str] = None
    barcode_2: Optional[str] = None
    asset_tag: Optional[str] = None
    remote_management: Optional[ClassicComputerGeneralRemoteManagement] = None
    supervised: Optional[bool] = None
    mdm_capable: Optional[bool] = None
    mdm_capable_users: Optional[Union[dict, ClassicComputerGeneralMdmCapableUsers]] = None
    management_status: Optional[ClassicComputerGeneralManagementStatus] = None
    report_date: Optional[str] = None
    report_date_epoch: Optional[int] = None
    report_date_utc: Union[Optional[datetime], Optional[str]] = None
    last_contact_time: Optional[str] = None
    last_contact_time_epoch: Optional[int] = None
    last_contact_time_utc: Optional[str] = None
    initial_entry_date: Optional[str] = None
    initial_entry_date_epoch: Optional[int] = None
    initial_entry_date_utc: Union[Optional[datetime], Optional[str]] = None
    last_cloud_backup_date_epoch: Optional[int] = None
    last_cloud_backup_date_utc: Union[Optional[datetime], Optional[str]] = None
    last_enrolled_date_epoch: Optional[int] = None
    last_enrolled_date_utc: Union[Optional[datetime], Optional[str]] = None
    mdm_profile_expiration_epoch: Optional[int] = None
    mdm_profile_expiration_utc: Union[Optional[datetime], Optional[str]] = None
    distribution_point: Optional[str] = None
    sus: Optional[str] = None
    site: Optional[ClassicSite] = None
    itunes_store_account_is_active: Optional[bool] = None


# Computer.Hardware Models


class ClassicComputerHardwareStorageDevicePartition(BaseModel):
    """Computer nested model: computer.hardware.storage.partitions"""

    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    partition_capacity_mb: Optional[int] = None
    percentage_full: Optional[int] = None
    available_mb: Optional[int] = None
    filevault_status: Optional[str] = None
    filevault_percent: Optional[int] = None
    filevault2_status: Optional[str] = None
    filevault2_percent: Optional[int] = None
    boot_drive_available_mb: Optional[int] = None
    lvgUUID: Optional[str] = None
    lvUUID: Optional[str] = None
    pvUUID: Optional[str] = None


class ClassicComputerHardwareStorageDevice(BaseModel):
    """Computer nested model: computer.hardware.storage"""

    model_config = ConfigDict(extra="allow")

    disk: Optional[str] = None
    model: Optional[str] = None
    revision: Optional[str] = None
    serial_number: Optional[str] = None
    size: Optional[int] = None
    drive_capacity_mb: Optional[int] = None
    connection_type: Optional[str] = None
    smart_status: Optional[str] = None
    partitions: Optional[List[ClassicComputerHardwareStorageDevicePartition]] = None


class ClassicComputerHardwareMappedPrinter(BaseModel):
    """Computer nested model: computer.hardware.mapped_printers"""

    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    uri: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None


class ClassicComputerHardware(ClassicApiModel):
    """Computer nested model: computer.hardware"""

    model_config = ConfigDict(extra="allow", protected_namespaces=())
    # The 'model_identifier' attribute conflicts with Pydantic's protect 'model_' namespace
    # Overriding 'protected_namespaces' for hardware suppresses the warning

    _xml_root_name = "hardware"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES

    make: Optional[str] = None
    model: Optional[str] = None
    model_identifier: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    os_build: Optional[str] = None
    software_update_device_id: Optional[str] = None
    active_directory_status: Optional[str] = None
    service_pack: Optional[str] = None
    processor_type: Optional[str] = None
    is_apple_silicon: Optional[bool] = None
    processor_architecture: Optional[str] = None
    processor_speed: Optional[int] = None
    processor_speed_mhz: Optional[int] = None
    number_processors: Optional[int] = None
    number_cores: Optional[int] = None
    total_ram: Optional[int] = None
    total_ram_mb: Optional[int] = None
    boot_rom: Optional[str] = None
    bus_speed: Optional[int] = None
    bus_speed_mhz: Optional[int] = None
    battery_capacity: Optional[int] = None
    cache_size: Optional[int] = None
    cache_size_kb: Optional[int] = None
    available_ram_slots: Optional[int] = None
    optical_drive: Optional[str] = None
    nic_speed: Optional[str] = None
    smc_version: Optional[str] = None
    ble_capable: Optional[bool] = None
    supports_ios_app_installs: Optional[bool] = None
    sip_status: Optional[str] = None
    gatekeeper_status: Optional[str] = None
    xprotect_version: Optional[str] = None
    institutional_recovery_key: Optional[str] = None
    disk_encryption_configuration: Optional[str] = None
    filevault2_users: Optional[List[str]] = None
    storage: Optional[List[ClassicComputerHardwareStorageDevice]] = None
    mapped_printers: Optional[List[ClassicComputerHardwareMappedPrinter]] = None


# Computer.Certificate Models


class ClassicComputerCertificate(BaseModel):
    """Computer nested model: computer.certificates"""

    model_config = ConfigDict(extra="allow")

    common_name: Optional[str] = None
    identity: Optional[bool] = None
    expires_utc: Optional[str] = None
    expires_epoch: Optional[int] = None
    name: Optional[str] = None


# Computer.Security Models


class ClassicComputerSecurity(BaseModel):
    """Computer nested model: computer.security"""

    model_config = ConfigDict(extra="allow")

    activation_lock: Optional[bool] = None
    recovery_lock_enabled: Optional[bool] = None
    secure_boot_level: Optional[str] = None
    external_boot_level: Optional[str] = None
    firewall_enabled: Optional[bool] = None


# Computer.Software Models


class ClassicComputerSoftwareAvailableUpdate(BaseModel):
    """Computer nested model: computer.software.available_updates"""

    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    package_name: Optional[str] = None
    version: Optional[str] = None


class ClassicComputerSoftwareItem(BaseModel):
    """Computer nested model: computer.software.applications, computer.software.fonts,
    computer.software.plugins
    """

    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    path: Optional[str] = None
    version: Optional[str] = None
    bundle_id: Optional[str] = None


class ClassicComputerSoftware(BaseModel):  # Lots of assumptions in this object
    """Computer nested model: computer.software"""

    model_config = ConfigDict(extra="allow")

    unix_executables: Optional[List[str]] = None
    licensed_software: Optional[List[str]] = None
    installed_by_casper: Optional[List[str]] = None
    installed_by_installer_swu: Optional[List[str]] = None
    cached_by_casper: Optional[List[str]] = None
    available_software_updates: Optional[List[str]] = None
    available_updates: Union[
        Optional[List[ClassicComputerSoftwareAvailableUpdate]], Optional[dict]
    ] = None
    running_services: Optional[List[str]] = None
    applications: Optional[List[ClassicComputerSoftwareItem]] = None
    fonts: Optional[List[ClassicComputerSoftwareItem]] = None
    plugins: Optional[List[ClassicComputerSoftwareItem]] = None


# Computer.ExtensionAttributes Models


class ClassicComputerExtensionAttribute(BaseModel):
    """Computer nested model: computer.extension_attributes"""

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    multi_value: Optional[bool] = None
    value: Optional[str] = None


# Computer GroupsAccounts Models


class ClassicComputerGroupsAccountsLocalAccount(BaseModel):
    """Computer nested model: computer.groups_accounts.local_accounts"""

    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    realname: Optional[str] = None
    uid: Optional[str] = None
    home: Optional[str] = None
    home_size: Optional[str] = None
    home_size_mb: Optional[int] = None
    administrator: Optional[bool] = None
    filevault_enabled: Optional[bool] = None


class ClassicComputerGroupsAccountsUserInventoriesUser(BaseModel):
    """Computer nested model: computer.groups_accounts.user_inventories.user"""

    model_config = ConfigDict(extra="allow")

    username: Optional[str] = None
    password_history_depth: Optional[str] = None
    password_min_length: Optional[str] = None
    password_max_age: Optional[str] = None
    password_min_complex_characters: Optional[str] = None
    password_require_alphanumeric: Optional[str] = None


class ClassicComputerGroupsAccountsUserInventories(BaseModel):
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

    model_config = ConfigDict(extra="allow")

    disable_automatic_login: Optional[bool] = None
    user: Union[
        Optional[ClassicComputerGroupsAccountsUserInventoriesUser],
        Optional[List[ClassicComputerGroupsAccountsUserInventoriesUser]],
    ] = None


class ClassicComputerGroupsAccounts(BaseModel):
    """Computer nested model: computer.groups_accounts"""

    model_config = ConfigDict(extra="allow")

    computer_group_memberships: Optional[List[str]] = None
    local_accounts: Optional[List[ClassicComputerGroupsAccountsLocalAccount]] = None
    user_inventories: Optional[ClassicComputerGroupsAccountsUserInventories] = None


# Computer.ConfigurationProfiles Models


class ClassicComputerConfigurationProfile(BaseModel):
    """Computer nested model: computer.configuration_profiles"""

    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    name: Optional[str] = None
    uuid: Optional[str] = None
    is_removable: Optional[bool] = None


# Computer Models


class ClassicComputersItem(BaseModel):
    """Represents a computer record returned by the
    :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_computers` operation.

    Unless the ``basic`` subset has been requested, only ``id`` and ``name`` will be
    populated.
    """

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    managed: Optional[bool] = None
    username: Optional[str] = None
    model: Optional[str] = None
    department: Optional[str] = None
    building: Optional[str] = None
    mac_address: Optional[str] = None
    udid: Optional[str] = None
    serial_number: Optional[str] = None
    report_date_utc: Union[Optional[datetime], Optional[str]] = None
    report_date_epoch: Optional[int] = None


class ClassicComputer(ClassicApiModel):
    """Represents a full computer inventory record.

    When exporting to XML for a ``POST``/``PUT`` operation, the SDK by default will only
    include ``general``, ``location``, and ``extension_attributes``. To bypass this
    behavior export the model using
    :meth:`~jamf_pro_sdk.models.classic.ClassicApiModel.xml` before pasting to the API
    operation.
    """

    model_config = ConfigDict(extra="allow")

    _xml_root_name = "computer"
    _xml_array_item_names = _XML_ARRAY_ITEM_NAMES
    _xml_write_fields = {"general", "location", "extension_attributes"}

    general: Optional[ClassicComputerGeneral] = Field(default_factory=ClassicComputerGeneral)
    location: Optional[ClassicDeviceLocation] = Field(default_factory=ClassicDeviceLocation)
    purchasing: Optional[ClassicDevicePurchasing] = None
    # Peripherals are a deprecated feature of Jamf Pro
    peripherals: Optional[Any] = None
    hardware: Optional[ClassicComputerHardware] = None
    certificates: Optional[List[ClassicComputerCertificate]] = None
    security: Optional[ClassicComputerSecurity] = None
    software: Optional[ClassicComputerSoftware] = None
    extension_attributes: Optional[List[ClassicComputerExtensionAttribute]] = Field(
        default_factory=list
    )
    groups_accounts: Optional[ClassicComputerGroupsAccounts] = None
    # iPhones in Computer inventory is a deprecated feature of Jamf Pro
    iphones: Optional[Any] = None
    configuration_profiles: Optional[List[ClassicComputerConfigurationProfile]] = None
