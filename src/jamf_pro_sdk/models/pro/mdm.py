from datetime import datetime
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Extra, Field, constr

from .api_options import get_mdm_commands_v2_allowed_command_types

# A note on MDM Command Types:
# The ``get_mdm_commands_v2_allowed_command_types`` list in the ``api_options`` file is referenced
# in the Jamf Pro OpenAPI schema (10.50) for allowed command types, but the API will reject all but
# a few allowed types.


# Enable Lost Mode Command


class EnableLostModeCommand(BaseModel):
    commandType: Literal["ENABLE_LOST_MODE"] = "ENABLE_LOST_MODE"
    lostModeMessage: str
    lostModePhone: str
    lostModeFootnote: str


# Erase Device Command Models


class EraseDeviceCommandObliterationBehavior(str, Enum):
    Default = "Default"
    DoNotObliterate = "DoNotObliterate"
    ObliterateWithWarning = "ObliterateWithWarning"
    Always = "Always"


class EraseDeviceCommandReturnToService(BaseModel):
    enabled: Literal[True]
    mdmProfileData: str
    wifiProfileData: str


class EraseDeviceCommand(BaseModel):
    commandType: Literal["ERASE_DEVICE"] = "ERASE_DEVICE"
    preserveDataPlan: Optional[bool]
    disallowProximitySetup: Optional[bool]
    pin: Optional[constr(min_length=6, max_length=6)]
    obliterationBehavior: Optional[EraseDeviceCommandObliterationBehavior]
    returnToService: Optional[EraseDeviceCommandReturnToService]


# Log Out User


class LogOutUserCommand(BaseModel):
    commandType: Literal["LOG_OUT_USER"] = "LOG_OUT_USER"


# Restart Device


class RestartDeviceCommand(BaseModel):
    commandType: Literal["RESTART_DEVICE"] = "RESTART_DEVICE"
    rebuildKernelCache: Optional[bool]
    kextPaths: Optional[List[str]]
    notifyUser: Optional[bool]


# Set Recovery Lock


class SetRecoveryLockCommand(BaseModel):
    commandType: Literal["SET_RECOVERY_LOCK"] = "SET_RECOVERY_LOCK"
    newPassword: str


# Shut Down Device


class ShutDownDeviceCommand(BaseModel):
    commandType: Literal["SHUT_DOWN_DEVICE"] = "SHUT_DOWN_DEVICE"


# Custom Command


class CustomCommand(BaseModel, extra=Extra.allow):
    """A free form model for new commands not yet supported by the SDK."""

    commandType: str


# MDM Send Command Models


class SendMdmCommandClientData(BaseModel):
    managementId: UUID


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


class SendMdmCommandResponse(BaseModel, extra=Extra.allow):
    id: str
    href: str


class RenewMdmProfileResponse(BaseModel, extra=Extra.allow):
    """This response model flattens the normal API JSON response from a nested
    ``udidsNotProcessed.uuids`` array to just ``udidsNotProcessed``.
    """

    udidsNotProcessed: Optional[List[UUID]]


# MDM Command Status Models


class MdmCommandStatusClientTypes(str, Enum):
    MOBILE_DEVICE = "MOBILE_DEVICE"
    TV = "TV"
    COMPUTER = "COMPUTER"
    COMPUTER_USER = "COMPUTER_USER"
    MOBILE_DEVICE_USER = "MOBILE_DEVICE_USER"


class MdmCommandStatusClient(BaseModel, extra=Extra.allow):
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


class MdmCommandStatus(BaseModel, extra=Extra.allow):
    uuid: UUID
    client: MdmCommandStatusClient
    commandState: MdmCommandStatusStates
    commandType: MdmCommandStatusTypes
    dateSent: datetime
    dateCompleted: datetime
    profileId: Optional[int]
