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


# Enable Lost Mode Command


class EnableLostModeCommand(BaseModel):
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


class EraseDeviceCommand(BaseModel):
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


class LogOutUserCommand(BaseModel):
    """MDM command to log a user out of the device.

    .. code-block:: python

        command = LogOutUserCommand()

    """

    commandType: Literal["LOG_OUT_USER"] = "LOG_OUT_USER"


# Restart Device


class RestartDeviceCommand(BaseModel):
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


class SetRecoveryLockCommand(BaseModel):
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


class ShutDownDeviceCommand(BaseModel):
    """MDM command to shut down a device.

    .. code-block:: python

        command = ShutDownDeviceCommand()

    """

    commandType: Literal["SHUT_DOWN_DEVICE"] = "SHUT_DOWN_DEVICE"


# Custom Command


class CustomCommand(BaseModel):
    """A free form model for new commands not yet supported by the SDK."""

    model_config = ConfigDict(extra="allow")

    commandType: str


# MDM Send Command Models


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
