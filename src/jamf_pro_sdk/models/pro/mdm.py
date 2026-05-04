from datetime import datetime
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from .api_options import get_mdm_commands_v2_allowed_command_types

# A note on MDM Command Types:
# The ``get_mdm_commands_v2_allowed_command_types`` list in the ``api_options`` file is referenced
# in the Jamf Pro OpenAPI schema (10.50) for allowed command types, but the API will reject all but
# a few allowed types.


# MDM Command Base
#
# All concrete MDM command models inherit from MdmCommand. This gives the
# public client API a single type to accept (`command: MdmCommand`) while
# the underlying ``MdmCommandRequest.commandData`` still validates against
# the discriminated ``BuiltInCommandsV2`` Union for serialization fidelity.


class MdmCommand(BaseModel):
    """Base class for all MDM command models. Concrete subclasses set a
    ``commandType`` Literal and may declare command-specific fields."""

    commandType: str


# Enable Lost Mode Command


class EnableLostModeCommand(MdmCommand):
    """MDM command to enable Lost Mode.

    .. code-block:: python

        command = EnableLostModeCommand()
        command.lostModeMessage = "Please return me to my owner."
        command.lostModePhone = "123-456-7890"
        command.lostModeFootnote = "No reward."

    Alternatively, unpack a dictionary:

    .. code-block:: python

        command = EnableLostModeCommand(
            **{
                "lostModeMessage": "Please return me to my owner.",
                "lostModePhone": "123-456-7890",
                "lostModeFootnote": "No reward."
            }
        )

    """

    commandType: Literal["ENABLE_LOST_MODE"] = "ENABLE_LOST_MODE"
    lostModeMessage: str
    lostModePhone: str
    lostModeFootnote: str


# Erase Device Command Models


class EraseDeviceCommandObliterationBehavior(str, Enum):
    """Define the fallback behavior for erasing a device."""

    Default = "Default"
    DoNotObliterate = "DoNotObliterate"
    ObliterateWithWarning = "ObliterateWithWarning"
    Always = "Always"


class EraseDeviceCommandReturnToService(BaseModel):
    """Configuration settings for Return to Service.

    The ``mdmProfileData`` and `w`ifiProfileData`` values must e base64 encoded strings.
    """

    enabled: Literal[True]
    # TODO: Add automatic conversion to base64 encoded profile if the provided data is a dictionary.
    mdmProfileData: str
    wifiProfileData: str


EraseDeviceCommandPin = Annotated[str, StringConstraints(min_length=6, max_length=6)]


class EraseDeviceCommand(MdmCommand):
    """MDM command to remotely wipe a device. Optionally, set the ``returnToService`` property to
    automatically connect to a wireless network at Setup Assistant.

        .. code-block:: python

            command = EraseDeviceCommand()
            command.pin = "123456"
            command.obliterationBehavior = EraseDeviceCommandObliterationBehavior.ObliterateWithWarning

    Alternatively, unpack a dictionary:

        .. code-block:: python

            command = EraseDeviceCommand(
                **{
                    "pin": "Please return me to my owner.",
                    "obliterationBehavior": "ObliterateWithWarning"
                }
            )
    """

    commandType: Literal["ERASE_DEVICE"] = "ERASE_DEVICE"
    preserveDataPlan: Optional[bool] = None
    disallowProximitySetup: Optional[bool] = None
    pin: Optional[EraseDeviceCommandPin] = None
    obliterationBehavior: Optional[EraseDeviceCommandObliterationBehavior] = None
    returnToService: Optional[EraseDeviceCommandReturnToService] = None


# Log Out User


class LogOutUserCommand(MdmCommand):
    """MDM command to log a user out of the device.

    .. code-block:: python

        command = LogOutUserCommand()

    """

    commandType: Literal["LOG_OUT_USER"] = "LOG_OUT_USER"


# Restart Device


class RestartDeviceCommand(MdmCommand):
    """MDM command to restart a device.

    ``kextPaths`` is only used if ``rebuildKernelCache`` is ``true``.

    .. code-block:: python

        command = RestartDeviceCommand()
        command.notifyUser = True

    Alternatively, unpack a dictionary:

    .. code-block:: python

        command = RestartDeviceCommand(
            **{
                "notifyUser": True
            }
        )
    """

    commandType: Literal["RESTART_DEVICE"] = "RESTART_DEVICE"
    rebuildKernelCache: Optional[bool]
    kextPaths: Optional[List[str]]
    notifyUser: Optional[bool]


# Set Recovery Lock


class SetRecoveryLockCommand(MdmCommand):
    """MDM command to set Recovery Lock on a device.

    Set ``newPassword`` to an empty string to clear the Recovery Lock password.

    .. code-block:: python

        command = SetRecoveryLockCommand()
        command.newPassword = "jamf1234"

    Alternatively, unpack a dictionary:

    .. code-block:: python

        command = SetRecoveryLockCommand(
            **{
                "newPassword": "jamf1234"
            }
        )

    """

    commandType: Literal["SET_RECOVERY_LOCK"] = "SET_RECOVERY_LOCK"
    newPassword: str


# Shut Down Device


class ShutDownDeviceCommand(MdmCommand):
    """MDM command to shut down a device.

    .. code-block:: python

        command = ShutDownDeviceCommand()

    """

    commandType: Literal["SHUT_DOWN_DEVICE"] = "SHUT_DOWN_DEVICE"


# Custom Command


class CustomCommand(MdmCommand):
    """A free form model for new commands not yet supported by the SDK."""

    model_config = ConfigDict(extra="allow")

    commandType: str


# V2 MDM Command Models


class ApplyRedemptionCodeCommand(MdmCommand):
    """MDM command to apply a redemption code to a device."""

    commandType: Literal["APPLY_REDEMPTION_CODE"] = "APPLY_REDEMPTION_CODE"
    redemptionCode: str


class CertificateListCommand(MdmCommand):
    """MDM command to request a certificate list from a device."""

    commandType: Literal["CERTIFICATE_LIST"] = "CERTIFICATE_LIST"


class ClearPasscodeCommand(MdmCommand):
    """MDM command to clear the passcode on a device."""

    commandType: Literal["CLEAR_PASSCODE"] = "CLEAR_PASSCODE"


class ClearRestrictionsPasswordCommand(MdmCommand):
    """MDM command to clear restrictions password on a device."""

    commandType: Literal["CLEAR_RESTRICTIONS_PASSWORD"] = "CLEAR_RESTRICTIONS_PASSWORD"


class DeclarativeManagementCommand(MdmCommand):
    """MDM command for declarative device management."""

    commandType: Literal["DECLARATIVE_MANAGEMENT"] = "DECLARATIVE_MANAGEMENT"


class DeleteUserCommand(MdmCommand):
    """MDM command to delete a user from a shared device."""

    commandType: Literal["DELETE_USER"] = "DELETE_USER"
    userName: Optional[str] = None
    forceDeletion: Optional[bool] = None


class DeviceInformationCommand(MdmCommand):
    """MDM command to request device information."""

    commandType: Literal["DEVICE_INFORMATION"] = "DEVICE_INFORMATION"


class DeviceLocationCommand(MdmCommand):
    """MDM command to request device location."""

    commandType: Literal["DEVICE_LOCATION"] = "DEVICE_LOCATION"


class DeviceLockCommand(MdmCommand):
    """MDM command to lock a device."""

    commandType: Literal["DEVICE_LOCK"] = "DEVICE_LOCK"
    pin: Optional[str] = None
    message: Optional[str] = None
    phoneNumber: Optional[str] = None


class DisableLostModeCommand(MdmCommand):
    """MDM command to disable Lost Mode on a device."""

    commandType: Literal["DISABLE_LOST_MODE"] = "DISABLE_LOST_MODE"


class DisableRemoteDesktopCommand(MdmCommand):
    """MDM command to disable Remote Desktop on a Mac."""

    commandType: Literal["DISABLE_REMOTE_DESKTOP"] = "DISABLE_REMOTE_DESKTOP"


class EnableRemoteDesktopCommand(MdmCommand):
    """MDM command to enable Remote Desktop on a Mac."""

    commandType: Literal["ENABLE_REMOTE_DESKTOP"] = "ENABLE_REMOTE_DESKTOP"


class InstalledApplicationListCommand(MdmCommand):
    """MDM command to request the list of installed applications."""

    commandType: Literal["INSTALLED_APPLICATION_LIST"] = "INSTALLED_APPLICATION_LIST"


class ManagedApplicationListCommand(MdmCommand):
    """MDM command to request the list of managed applications."""

    commandType: Literal["MANAGED_APPLICATION_LIST"] = "MANAGED_APPLICATION_LIST"


class ManagedMediaListCommand(MdmCommand):
    """MDM command to request the list of managed media."""

    commandType: Literal["MANAGED_MEDIA_LIST"] = "MANAGED_MEDIA_LIST"


class PlayLostModeSoundCommand(MdmCommand):
    """MDM command to play a sound on a device in Lost Mode."""

    commandType: Literal["PLAY_LOST_MODE_SOUND"] = "PLAY_LOST_MODE_SOUND"


class ProvisioningProfileListCommand(MdmCommand):
    """MDM command to request the list of provisioning profiles."""

    commandType: Literal["PROVISIONING_PROFILE_LIST"] = "PROVISIONING_PROFILE_LIST"


class RefreshCellularPlansCommand(MdmCommand):
    """MDM command to refresh cellular plans on a device."""

    commandType: Literal["REFRESH_CELLULAR_PLANS"] = "REFRESH_CELLULAR_PLANS"


class RequestMirroringCommand(MdmCommand):
    """MDM command to request AirPlay mirroring."""

    commandType: Literal["REQUEST_MIRRORING"] = "REQUEST_MIRRORING"


class SecurityInfoCommand(MdmCommand):
    """MDM command to request security information from a device."""

    commandType: Literal["SECURITY_INFO"] = "SECURITY_INFO"


class SetAutoAdminPasswordCommand(MdmCommand):
    """MDM command to set the auto admin password."""

    commandType: Literal["SET_AUTO_ADMIN_PASSWORD"] = "SET_AUTO_ADMIN_PASSWORD"
    guid: str
    password: str


class SettingsCommand(MdmCommand):
    """MDM command to update device settings."""

    model_config = ConfigDict(extra="allow")

    commandType: Literal["SETTINGS"] = "SETTINGS"


class StopMirroringCommand(MdmCommand):
    """MDM command to stop AirPlay mirroring."""

    commandType: Literal["STOP_MIRRORING"] = "STOP_MIRRORING"


class UnlockUserAccountCommand(MdmCommand):
    """MDM command to unlock a user account on a device."""

    commandType: Literal["UNLOCK_USER_ACCOUNT"] = "UNLOCK_USER_ACCOUNT"
    userName: str


class ValidateApplicationsCommand(MdmCommand):
    """MDM command to validate managed applications on a device."""

    commandType: Literal["VALIDATE_APPLICATIONS"] = "VALIDATE_APPLICATIONS"


class VerifyRecoveryLockCommand(MdmCommand):
    """MDM command to verify the Recovery Lock password on a device."""

    commandType: Literal["VERIFY_RECOVERY_LOCK"] = "VERIFY_RECOVERY_LOCK"
    password: str


# MDM Send Command Models (Preview - Deprecated)


class SendMdmCommandClientData(BaseModel):
    managementId: Union[str, UUID]


BuiltInCommands = Annotated[
    Union[
        EnableLostModeCommand,
        EraseDeviceCommand,
        LogOutUserCommand,
        RestartDeviceCommand,
        SetRecoveryLockCommand,
        ShutDownDeviceCommand,
    ],
    Field(..., discriminator="commandType"),
]


class SendMdmCommand(BaseModel):
    clientData: List[SendMdmCommandClientData]
    commandData: Union[BuiltInCommands, CustomCommand]


# MDM Send Command Models (V2)


class MdmCommandClientRequest(BaseModel):
    managementId: Union[str, UUID]


BuiltInCommandsV2 = Annotated[
    Union[
        ApplyRedemptionCodeCommand,
        CertificateListCommand,
        ClearPasscodeCommand,
        ClearRestrictionsPasswordCommand,
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
    ],
    Field(..., discriminator="commandType"),
]


class MdmCommandRequest(BaseModel):
    clientData: List[MdmCommandClientRequest]
    commandData: Union[BuiltInCommandsV2, CustomCommand]


# MDM Command Responses


class SendMdmCommandResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    href: str


class RenewMdmProfileResponse(BaseModel):
    """This response model flattens the normal API JSON response from a nested
    ``udidsNotProcessed.uuids`` array to just ``udidsNotProcessed``.
    """

    model_config = ConfigDict(extra="allow")

    udidsNotProcessed: Optional[List[UUID]]


# MDM Command Status Models


class MdmCommandStatusClientTypes(str, Enum):
    MOBILE_DEVICE = "MOBILE_DEVICE"
    TV = "TV"
    COMPUTER = "COMPUTER"
    COMPUTER_USER = "COMPUTER_USER"
    MOBILE_DEVICE_USER = "MOBILE_DEVICE_USER"


class MdmCommandStatusClient(BaseModel):
    model_config = ConfigDict(extra="allow")

    managementId: UUID
    clientType: MdmCommandStatusClientTypes


class MdmCommandStatusStates(str, Enum):
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    NOT_NOW = "NOT_NOW"
    ERROR = "ERROR"


# Enum created from values in API Options
MdmCommandStatusTypes = Enum(
    "MdmCommandStatusTypes", {i: i for i in get_mdm_commands_v2_allowed_command_types}
)


class MdmCommandStatus(BaseModel):
    model_config = ConfigDict(extra="allow")

    uuid: UUID
    client: MdmCommandStatusClient
    commandState: MdmCommandStatusStates
    commandType: MdmCommandStatusTypes
    dateSent: datetime
    dateCompleted: datetime
    profileId: Optional[int] = None
