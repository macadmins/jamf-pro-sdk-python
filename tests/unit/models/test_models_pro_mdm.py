import json

from src.jamf_pro_sdk.models.pro.mdm import (
    ApplyRedemptionCodeCommand,
    CertificateListCommand,
    ClearPasscodeCommand,
    ClearRestrictionsPasswordCommand,
    CustomCommand,
    DeclarativeManagementCommand,
    DeleteUserCommand,
    DeviceInformationCommand,
    DeviceLocationCommand,
    DeviceLockCommand,
    DisableLostModeCommand,
    DisableRemoteDesktopCommand,
    EnableLostModeCommand,
    EnableRemoteDesktopCommand,
    EraseDeviceCommand,
    InstalledApplicationListCommand,
    LogOutUserCommand,
    ManagedApplicationListCommand,
    ManagedMediaListCommand,
    MdmCommandClientRequest,
    MdmCommandRequest,
    PlayLostModeSoundCommand,
    ProvisioningProfileListCommand,
    RefreshCellularPlansCommand,
    RequestMirroringCommand,
    RestartDeviceCommand,
    SecurityInfoCommand,
    SetAutoAdminPasswordCommand,
    SetRecoveryLockCommand,
    SettingsCommand,
    ShutDownDeviceCommand,
    StopMirroringCommand,
    UnlockUserAccountCommand,
    ValidateApplicationsCommand,
    VerifyRecoveryLockCommand,
)

# Simple commands (no required fields beyond commandType)

SIMPLE_COMMANDS = [
    (CertificateListCommand, "CERTIFICATE_LIST"),
    (ClearPasscodeCommand, "CLEAR_PASSCODE"),
    (ClearRestrictionsPasswordCommand, "CLEAR_RESTRICTIONS_PASSWORD"),
    (DeclarativeManagementCommand, "DECLARATIVE_MANAGEMENT"),
    (DeviceInformationCommand, "DEVICE_INFORMATION"),
    (DeviceLocationCommand, "DEVICE_LOCATION"),
    (DisableLostModeCommand, "DISABLE_LOST_MODE"),
    (DisableRemoteDesktopCommand, "DISABLE_REMOTE_DESKTOP"),
    (EnableRemoteDesktopCommand, "ENABLE_REMOTE_DESKTOP"),
    (InstalledApplicationListCommand, "INSTALLED_APPLICATION_LIST"),
    (LogOutUserCommand, "LOG_OUT_USER"),
    (ManagedApplicationListCommand, "MANAGED_APPLICATION_LIST"),
    (ManagedMediaListCommand, "MANAGED_MEDIA_LIST"),
    (PlayLostModeSoundCommand, "PLAY_LOST_MODE_SOUND"),
    (ProvisioningProfileListCommand, "PROVISIONING_PROFILE_LIST"),
    (RefreshCellularPlansCommand, "REFRESH_CELLULAR_PLANS"),
    (RequestMirroringCommand, "REQUEST_MIRRORING"),
    (SecurityInfoCommand, "SECURITY_INFO"),
    (ShutDownDeviceCommand, "SHUT_DOWN_DEVICE"),
    (StopMirroringCommand, "STOP_MIRRORING"),
    (ValidateApplicationsCommand, "VALIDATE_APPLICATIONS"),
]


def test_simple_command_defaults():
    """All simple commands should have the correct commandType default."""
    for command_cls, expected_type in SIMPLE_COMMANDS:
        command = command_cls()
        assert command.commandType == expected_type


def test_simple_command_serialization():
    """Simple commands should serialize to a dict with only commandType."""
    for command_cls, expected_type in SIMPLE_COMMANDS:
        command = command_cls()
        data = json.loads(command.model_dump_json(exclude_none=True))
        assert data == {"commandType": expected_type}


def test_enable_lost_mode_command():
    command = EnableLostModeCommand(
        lostModeMessage="Return me",
        lostModePhone="555-1234",
        lostModeFootnote="No reward",
    )
    assert command.commandType == "ENABLE_LOST_MODE"
    assert command.lostModeMessage == "Return me"
    assert command.lostModePhone == "555-1234"
    assert command.lostModeFootnote == "No reward"


def test_erase_device_command():
    command = EraseDeviceCommand(pin="123456", obliterationBehavior="ObliterateWithWarning")
    assert command.commandType == "ERASE_DEVICE"
    assert command.pin == "123456"
    assert command.obliterationBehavior.value == "ObliterateWithWarning"


def test_erase_device_command_optional_fields():
    command = EraseDeviceCommand()
    assert command.commandType == "ERASE_DEVICE"
    assert command.pin is None
    assert command.obliterationBehavior is None
    assert command.returnToService is None


def test_restart_device_command():
    command = RestartDeviceCommand(notifyUser=True, rebuildKernelCache=False, kextPaths=None)
    assert command.commandType == "RESTART_DEVICE"
    assert command.notifyUser is True
    assert command.rebuildKernelCache is False


def test_set_recovery_lock_command():
    command = SetRecoveryLockCommand(newPassword="jamf1234")
    assert command.commandType == "SET_RECOVERY_LOCK"
    assert command.newPassword == "jamf1234"


def test_device_lock_command():
    command = DeviceLockCommand(pin="123456", message="Locked", phoneNumber="555-0000")
    assert command.commandType == "DEVICE_LOCK"
    assert command.pin == "123456"
    assert command.message == "Locked"
    assert command.phoneNumber == "555-0000"


def test_delete_user_command():
    command = DeleteUserCommand(userName="testuser", forceDeletion=True)
    assert command.commandType == "DELETE_USER"
    assert command.userName == "testuser"
    assert command.forceDeletion is True


def test_set_auto_admin_password_command():
    command = SetAutoAdminPasswordCommand(guid="abc-123", password="secret")
    assert command.commandType == "SET_AUTO_ADMIN_PASSWORD"
    assert command.guid == "abc-123"
    assert command.password == "secret"


def test_apply_redemption_code_command():
    command = ApplyRedemptionCodeCommand(redemptionCode="ABCD-1234")
    assert command.commandType == "APPLY_REDEMPTION_CODE"
    assert command.redemptionCode == "ABCD-1234"


def test_unlock_user_account_command():
    command = UnlockUserAccountCommand(userName="lockeduser")
    assert command.commandType == "UNLOCK_USER_ACCOUNT"
    assert command.userName == "lockeduser"


def test_verify_recovery_lock_command():
    command = VerifyRecoveryLockCommand(password="jamf1234")
    assert command.commandType == "VERIFY_RECOVERY_LOCK"
    assert command.password == "jamf1234"


def test_settings_command_allows_extra_fields():
    command = SettingsCommand(voiceRoaming=True, dataRoaming=False)
    assert command.commandType == "SETTINGS"
    assert command.voiceRoaming is True
    assert command.dataRoaming is False


def test_custom_command():
    command = CustomCommand(commandType="MY_CUSTOM_COMMAND", customField="value")
    assert command.commandType == "MY_CUSTOM_COMMAND"
    assert command.customField == "value"


# MdmCommandRequest tests


def test_mdm_command_request_with_simple_command():
    request = MdmCommandRequest(
        clientData=[MdmCommandClientRequest(managementId="4eecc1fb-f52d-48c5-9560-c246b23601d3")],
        commandData=LogOutUserCommand(),
    )
    assert len(request.clientData) == 1
    assert str(request.clientData[0].managementId) == "4eecc1fb-f52d-48c5-9560-c246b23601d3"
    assert request.commandData.commandType == "LOG_OUT_USER"


def test_mdm_command_request_multiple_devices():
    request = MdmCommandRequest(
        clientData=[
            MdmCommandClientRequest(managementId="aaaa-bbbb"),
            MdmCommandClientRequest(managementId="cccc-dddd"),
        ],
        commandData=ShutDownDeviceCommand(),
    )
    assert len(request.clientData) == 2


def test_mdm_command_request_serialization():
    request = MdmCommandRequest(
        clientData=[MdmCommandClientRequest(managementId="4eecc1fb-f52d-48c5-9560-c246b23601d3")],
        commandData=SetRecoveryLockCommand(newPassword="test123"),
    )
    data = json.loads(request.model_dump_json())
    assert data["clientData"][0]["managementId"] == "4eecc1fb-f52d-48c5-9560-c246b23601d3"
    assert data["commandData"]["commandType"] == "SET_RECOVERY_LOCK"
    assert data["commandData"]["newPassword"] == "test123"


def test_mdm_command_request_with_custom_command():
    request = MdmCommandRequest(
        clientData=[MdmCommandClientRequest(managementId="test-id")],
        commandData=CustomCommand(commandType="FUTURE_COMMAND", someField="value"),
    )
    assert request.commandData.commandType == "FUTURE_COMMAND"


def test_mdm_command_request_parsing_from_dict():
    """Verify MdmCommandRequest can be constructed from a raw dict."""
    raw = {
        "clientData": [{"managementId": "id-1"}, {"managementId": "id-2"}],
        "commandData": {"commandType": "ERASE_DEVICE", "pin": "654321"},
    }
    request = MdmCommandRequest.model_validate(raw)
    assert len(request.clientData) == 2
    assert request.commandData.commandType == "ERASE_DEVICE"
    assert request.commandData.pin == "654321"
