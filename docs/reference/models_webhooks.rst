:tocdepth: 2

Webhook Models
==============

.. note::

    The intended use of SDK models is to provide an easier developer experience when working with
    requests and responses. All fields are optional, and extra fields are allowed for when Jamf
    releases a new version that adds additional fields that are not yet reflected in the SDK. These
    extra fields when present may or may not reflect their actual types. Do not rely solely on the
    SDK models for data validation.

Webhooks
--------

.. currentmodule:: jamf_pro_sdk.models.webhooks.webhooks

.. autosummary::
    :toctree: _autosummary

    ComputerAdded
    ComputerCheckIn
    ComputerInventoryCompleted
    ComputerPolicyFinished
    ComputerPushCapabilityChanged
    DeviceAddedToDep
    JssShutdown
    JssStartup
    MobileDeviceCheckIn
    MobileDeviceEnrolled
    MobileDevicePushSent
    MobileDeviceUnEnrolled
    PushSent
    RestApiOperation
    SmartGroupComputerMembershipChange
    SmartGroupMobileDeviceMembershipChange
    SmartGroupUserMembershipChange

Event Models
------------

.. currentmodule:: jamf_pro_sdk.models.webhooks.webhooks

.. autosummary::
    :toctree: _autosummary

    WebhookData
    ComputerEvent
    MobileDeviceEvent
    ComputerAddedWebhook
    ComputerCheckInWebhook
    ComputerCheckInEvent
    ComputerInventoryCompletedWebhook
    ComputerPolicyFinishedWebhook
    ComputerPolicyFinishedEvent
    ComputerPushCapabilityChangedWebhook
    DeviceAddedToDepWebhook
    DeviceAddedToDepEvent
    JssShutdownWebhook
    JssStartupWebhook
    JssStartupShutdownEvent
    MobileDeviceCheckInWebhook
    MobileDeviceEnrolledWebhook
    MobileDevicePushSentWebhook
    MobileDeviceUnEnrolledWebhook
    PushSentWebhook
    PushSentEvent
    RestApiOperationWebhook
    RestApiOperationEvent
    SmartGroupComputerMembershipChangeWebhook
    SmartGroupComputerMembershipChangeEvent
    SmartGroupMobileDeviceMembershipChangeWebhook
    SmartGroupMobileDeviceMembershipChangeEvent
    SmartGroupUserMembershipChangeWebhook
    SmartGroupUserMembershipChangeEvent
