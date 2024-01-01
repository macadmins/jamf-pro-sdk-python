import re
from ipaddress import IPv4Address

from jamf_pro_sdk.clients.webhooks import get_webhook_generator
from jamf_pro_sdk.models.webhooks import (
    ComputerAdded,
    ComputerCheckIn,
    ComputerInventoryCompleted,
    ComputerPolicyFinished,
    ComputerPushCapabilityChanged,
    DeviceAddedToDep,
    JssShutdown,
    JssStartup,
    MobileDeviceCheckIn,
    MobileDeviceEnrolled,
    MobileDevicePushSent,
    MobileDeviceUnEnrolled,
    PushSent,
    RestApiOperation,
    SmartGroupComputerMembershipChange,
    SmartGroupMobileDeviceMembershipChange,
    SmartGroupUserMembershipChange,
)
from jamf_pro_sdk.models.webhooks.webhooks import ComputerEvent

MAC_REGEX = re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}(?:[0-9A-Fa-f]{2})$")
SERIAL_REGEX = re.compile(r"^[0-9A-Za-z]{10}$")
# Only assert for uppercase UUIDs
UUID_REGEX = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$")


def test_webhooks_computer_added():
    generator = get_webhook_generator(ComputerAdded)
    computer = generator.build()

    assert isinstance(computer, ComputerAdded)
    assert computer.webhook.webhookEvent == "ComputerAdded"

    # These fields will not be re-tested for any other events that share the same type
    assert isinstance(computer.event.ipAddress, IPv4Address)
    assert isinstance(computer.event.reportedIpAddress, IPv4Address)
    assert MAC_REGEX.match(computer.event.alternateMacAddress)
    assert MAC_REGEX.match(computer.event.macAddress)
    assert SERIAL_REGEX.match(computer.event.serialNumber)
    assert UUID_REGEX.match(computer.event.udid)


def test_webhooks_computer_checkin():
    generator = get_webhook_generator(ComputerCheckIn)
    computer = generator.build()

    assert isinstance(computer, ComputerCheckIn)
    assert computer.webhook.webhookEvent == "ComputerCheckIn"
    # Computer data is nested in this event type
    assert isinstance(computer.event.computer, ComputerEvent)


def test_webhooks_computer_inventory_completed():
    generator = get_webhook_generator(ComputerInventoryCompleted)
    computer = generator.build()

    assert isinstance(computer, ComputerInventoryCompleted)
    assert computer.webhook.webhookEvent == "ComputerInventoryCompleted"


def test_webhooks_computer_policy_finished():
    generator = get_webhook_generator(ComputerPolicyFinished)
    computer = generator.build()

    assert isinstance(computer, ComputerPolicyFinished)
    assert computer.webhook.webhookEvent == "ComputerPolicyFinished"
    # Computer data is nested in this event type
    assert isinstance(computer.event.computer, ComputerEvent)


def test_webhooks_computer_push_capability_changed():
    generator = get_webhook_generator(ComputerPushCapabilityChanged)
    computer = generator.build()

    assert isinstance(computer, ComputerPushCapabilityChanged)
    assert computer.webhook.webhookEvent == "ComputerPushCapabilityChanged"


def test_webhooks_device_added_to_dep():
    generator = get_webhook_generator(DeviceAddedToDep)
    dep_event = generator.build()

    assert isinstance(dep_event, DeviceAddedToDep)
    assert dep_event.webhook.webhookEvent == "DeviceAddedToDEP"


def test_webhooks_jss_startup():
    generator = get_webhook_generator(JssStartup)
    startup_event = generator.build()

    assert isinstance(startup_event, JssStartup)
    assert startup_event.webhook.webhookEvent == "JSSStartup"


def test_webhooks_jss_shutdown():
    generator = get_webhook_generator(JssShutdown)
    shutdown_event = generator.build()

    assert isinstance(shutdown_event, JssShutdown)
    assert shutdown_event.webhook.webhookEvent == "JSSShutdown"


def test_webhooks_mobile_device_checkin():
    generator = get_webhook_generator(MobileDeviceCheckIn)
    mobile_device = generator.build()

    assert isinstance(mobile_device, MobileDeviceCheckIn)
    assert mobile_device.webhook.webhookEvent == "MobileDeviceCheckIn"

    # These fields will not be re-tested for any other events that share the same type
    assert isinstance(mobile_device.event.ipAddress, IPv4Address)
    assert MAC_REGEX.match(mobile_device.event.bluetoothMacAddress)
    assert SERIAL_REGEX.match(mobile_device.event.serialNumber)
    assert UUID_REGEX.match(mobile_device.event.udid)
    assert MAC_REGEX.match(mobile_device.event.wifiMacAddress)


def test_webhooks_mobile_device_enrolled():
    generator = get_webhook_generator(MobileDeviceEnrolled)
    mobile_device = generator.build()

    assert isinstance(mobile_device, MobileDeviceEnrolled)
    assert mobile_device.webhook.webhookEvent == "MobileDeviceEnrolled"


def test_webhooks_mobile_device_unenrolled():
    generator = get_webhook_generator(MobileDeviceUnEnrolled)
    mobile_device = generator.build()

    assert isinstance(mobile_device, MobileDeviceUnEnrolled)
    assert mobile_device.webhook.webhookEvent == "MobileDeviceUnEnrolled"


def test_webhooks_mobile_device_push_sent():
    generator = get_webhook_generator(MobileDevicePushSent)
    mobile_device = generator.build()

    assert isinstance(mobile_device, MobileDevicePushSent)
    assert mobile_device.webhook.webhookEvent == "MobileDevicePushSent"


def test_webhooks_push_sent():
    generator = get_webhook_generator(PushSent)
    push_event = generator.build()

    assert isinstance(push_event, PushSent)
    assert push_event.webhook.webhookEvent == "PushSent"


def test_webhooks_rest_api_op():
    generator = get_webhook_generator(RestApiOperation)
    rest_api_op = generator.build()

    assert isinstance(rest_api_op, RestApiOperation)
    assert rest_api_op.webhook.webhookEvent == "RestAPIOperation"


def test_webhooks_smart_group_computer_membership_change():
    generator = get_webhook_generator(SmartGroupComputerMembershipChange)
    group_change = generator.build()

    assert isinstance(group_change, SmartGroupComputerMembershipChange)
    assert group_change.webhook.webhookEvent == "SmartGroupComputerMembershipChange"
    assert isinstance(group_change.event.computer, bool) and group_change.event.computer is True
    assert isinstance(group_change.event.smartGroup, bool) and group_change.event.smartGroup is True


def test_webhooks_smart_group_mobile_device_membership_change():
    generator = get_webhook_generator(SmartGroupMobileDeviceMembershipChange)
    group_change = generator.build()

    assert isinstance(group_change, SmartGroupMobileDeviceMembershipChange)
    assert group_change.webhook.webhookEvent == "SmartGroupMobileDeviceMembershipChange"
    assert isinstance(group_change.event.computer, bool) and group_change.event.computer is False
    assert isinstance(group_change.event.smartGroup, bool) and group_change.event.smartGroup is True


def test_webhooks_smart_group_user_membership_change():
    generator = get_webhook_generator(SmartGroupUserMembershipChange)
    group_change = generator.build()

    assert isinstance(group_change, SmartGroupUserMembershipChange)
    assert group_change.webhook.webhookEvent == "SmartGroupUserMembershipChange"
    assert not hasattr(group_change.event, "computer")
    assert isinstance(group_change.event.smartGroup, bool) and group_change.event.smartGroup is True
