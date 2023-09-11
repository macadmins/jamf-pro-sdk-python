from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra

from .api_options import get_mdm_commands_v2_allowed_command_types


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
