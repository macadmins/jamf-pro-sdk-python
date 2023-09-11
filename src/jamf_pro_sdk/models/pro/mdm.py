from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Extra, Field, constr

from .api_options import get_mdm_commands_v2_allowed_command_types


# Enable Lost Mode Command


class EnableLostModeCommand(BaseModel):
    commandType: Literal["EnableLostModeCommand"]
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
    commandType: Literal["EraseDeviceCommand"]
    preserveDataPlan: Optional[bool]
    disallowProximitySetup: Optional[bool]
    pin: Optional[constr(min_length=6, max_length=6)]
    obliterationBehavior: Optional[EraseDeviceCommandObliterationBehavior]
    returnToService: Optional[EraseDeviceCommandReturnToService]


# Restart Device


class RestartDeviceCommand(BaseModel):
    commandType: Literal["RestartDeviceCommand"]
    rebuildKernelCache: Optional[bool]
    kextPaths: Optional[List[str]]
    notifyUser: Optional[bool]


# Shut Down Device


class ShutDownDeviceCommand(BaseModel):
    commandType: Literal["ShutDownDeviceCommand"]


# MDM Send Command Models


class SendMdmCommandClientData(BaseModel):
    managementId: UUID


class SendMdmCommand(BaseModel):
    clientData: SendMdmCommandClientData
    commandData: Union[
        EnableLostModeCommand,
        EraseDeviceCommand,
        RestartDeviceCommand,
        ShutDownDeviceCommand,
    ] = Field(..., discriminator="commandType")


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
