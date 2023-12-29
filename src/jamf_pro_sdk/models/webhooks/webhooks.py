from ipaddress import IPv4Address
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict


class WebhookModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class WebhookData(WebhookModel):
    """Attributes shared by all Event models."""

    eventTimestamp: int
    id: int
    name: str


class ComputerEvent(WebhookModel):
    alternateMacAddress: str
    building: str
    department: str
    deviceName: str
    emailAddress: str
    ipAddress: IPv4Address
    jssID: int
    macAddress: str
    model: str
    osBuild: str
    osVersion: str
    phone: str
    position: str
    realName: str
    reportedIpAddress: IPv4Address
    room: str
    serialNumber: str
    udid: str
    userDirectoryID: str
    username: str


class MobileDeviceEvent(WebhookModel):
    bluetoothMacAddress: str
    deviceName: str
    icciID: str
    imei: str
    ipAddress: IPv4Address
    jssID: int
    model: str
    modelDisplay: str
    osBuild: str
    osVersion: str
    product: str
    room: str
    serialNumber: str
    udid: str
    userDirectoryID: str
    username: str
    version: str
    wifiMacAddress: str


# COMPUTER ADDED


class ComputerAddedWebhook(WebhookData):
    webhookEvent: Literal["ComputerAdded"]


class ComputerAdded(WebhookModel):
    webhook: ComputerAddedWebhook
    event: ComputerEvent


# COMPUTER CHECK-IN


class ComputerCheckInWebhook(WebhookData):
    webhookEvent: Literal["ComputerCheckIn"]


class ComputerCheckInEvent(WebhookModel):
    computer: ComputerEvent
    trigger: str
    username: str


class ComputerCheckIn(WebhookModel):
    webhook: ComputerCheckInWebhook
    event: ComputerCheckInEvent


# COMPUTER INVENTORY COMPLETED


class ComputerInventoryCompletedWebhook(WebhookData):
    webhookEvent: Literal["ComputerInventoryCompleted"]


class ComputerInventoryCompleted(WebhookModel):
    webhook: ComputerInventoryCompletedWebhook
    event: ComputerEvent


# COMPUTER POLICY FINISHED


class ComputerPolicyFinishedWebhook(WebhookData):
    webhookEvent: Literal["ComputerPolicyFinished"]


class ComputerPolicyFinishedEvent(WebhookModel):
    computer: ComputerEvent
    policyId: int
    successful: bool


class ComputerPolicyFinished(WebhookModel):
    webhook: ComputerPolicyFinishedWebhook
    event: ComputerPolicyFinishedEvent


# COMPUTER PUSH CAPABILITY CHANGED


class ComputerPushCapabilityChangedWebhook(WebhookData):
    webhookEvent: Literal["ComputerPushCapabilityChanged"]


class ComputerPushCapabilityChanged(WebhookModel):
    webhook: ComputerPushCapabilityChangedWebhook
    event: ComputerEvent


# DEVICE ADDED TO DEP


class DeviceAddedToDepWebhook(WebhookData):
    webhookEvent: Literal["DeviceAddedToDEP"]


class DeviceAddedToDepEvent(WebhookModel):
    assetTag: str
    description: str
    deviceAssignedDate: int
    deviceEnrollmentProgramInstanceId: int
    model: str
    serialNumber: str


class DeviceAddedToDep(WebhookModel):
    webhook: DeviceAddedToDepWebhook
    event: DeviceAddedToDepEvent


# JSS STARTUP/SHUTDOWN


class JssStartupWebhook(WebhookData):
    webhookEvent: Literal["JSSStartup"]


class JssShutdownWebhook(WebhookData):
    webhookEvent: Literal["JSSShutdown"]


class JssStartupShutdownEvent(WebhookModel):
    hostAddress: str
    institution: str
    isClusterMaster: bool
    jssUrl: str
    webApplicationPath: str


class JssStartup(WebhookModel):
    webhook: JssStartupWebhook
    event: JssStartupShutdownEvent


class JssShutdown(WebhookModel):
    webhook: JssShutdownWebhook
    event: JssStartupShutdownEvent


# MOBILE DEVICE CHECK-IN


class MobileDeviceCheckInWebhook(WebhookData):
    webhookEvent: Literal["MobileDeviceCheckIn"]


class MobileDeviceCheckIn(WebhookModel):
    webhook: MobileDeviceCheckInWebhook
    event: MobileDeviceEvent


# MOBILE DEVICE ENROLLED


class MobileDeviceEnrolledWebhook(WebhookData):
    webhookEvent: Literal["MobileDeviceEnrolled"]


class MobileDeviceEnrolled(WebhookModel):
    webhook: MobileDeviceEnrolledWebhook
    event: MobileDeviceEvent


# MOBILE DEVICE UNENROLLED


class MobileDeviceUnEnrolledWebhook(WebhookData):
    webhookEvent: Literal["MobileDeviceUnEnrolled"]


class MobileDeviceUnEnrolled(WebhookModel):
    webhook: MobileDeviceUnEnrolledWebhook
    event: MobileDeviceEvent


# MOBILE DEVICE PUSH SENT


class MobileDevicePushSentWebhook(WebhookData):
    webhookEvent: Literal["MobileDevicePushSent"]


class MobileDevicePushSent(WebhookModel):
    webhook: MobileDevicePushSentWebhook
    event: MobileDeviceEvent


# PUSH SENT


class PushSentWebhook(WebhookData):
    webhookEvent: Literal["PushSent"]


class PushSentEvent(WebhookModel):
    managementId: Union[int, str]
    type: str


class PushSent(WebhookModel):
    webhook: PushSentWebhook
    event: PushSentEvent


# REST API OPERATION


class RestApiOperationWebhook(WebhookData):
    webhookEvent: Literal["RestAPIOperation"]


class RestApiOperationEvent(WebhookModel):
    authorizedUsername: str
    objectID: int
    objectName: str
    objectTypeName: str
    operationSuccessful: bool
    restAPIOperationType: str


class RestApiOperation(WebhookModel):
    webhook: RestApiOperationWebhook
    event: RestApiOperationEvent


# COMPUTER SMART GROUP MEMBERSHIP CHANGE


class SmartGroupComputerMembershipChangeWebhook(WebhookData):
    webhookEvent: Literal["SmartGroupComputerMembershipChange"]


class SmartGroupComputerMembershipChangeEvent(WebhookModel):
    computer: Literal[True]
    groupAddedDevices: list
    groupAddedDevicesIds: list[int]
    groupRemovedDevices: list
    groupRemovedDevicesIds: list[int]
    jssid: int
    name: str
    smartGroup: Literal[True]


class SmartGroupComputerMembershipChange(WebhookModel):
    webhook: SmartGroupComputerMembershipChangeWebhook
    event: SmartGroupComputerMembershipChangeEvent


# MOBILE DEVICE SMART GROUP MEMBERSHIP CHANGE


class SmartGroupMobileDeviceMembershipChangeWebhook(WebhookData):
    webhookEvent: Literal["SmartGroupMobileDeviceMembershipChange"]


class SmartGroupMobileDeviceMembershipChangeEvent(WebhookModel):
    computer: Literal[False]
    groupAddedDevices: list[Optional[dict[str, str]]]
    groupAddedDevicesIds: list[int]
    groupRemovedDevices: list[Optional[dict[str, str]]]
    groupRemovedDevicesIds: list[int]
    jssid: int
    name: str
    smartGroup: Literal[True]


class SmartGroupMobileDeviceMembershipChange(WebhookModel):
    webhook: SmartGroupMobileDeviceMembershipChangeWebhook
    event: SmartGroupMobileDeviceMembershipChangeEvent


# USER SMART GROUP MEMBERSHIP CHANGE


class SmartGroupUserMembershipChangeWebhook(WebhookData):
    webhookEvent: Literal["SmartGroupUserMembershipChange"]


class SmartGroupUserMembershipChangeEvent(WebhookModel):
    groupAddedUserIds: list[int]
    groupRemovedUserIds: list[int]
    jssid: int
    name: str
    smartGroup: Literal[True]


class SmartGroupUserMembershipChange(WebhookModel):
    webhook: SmartGroupUserMembershipChangeWebhook
    event: SmartGroupUserMembershipChangeEvent
