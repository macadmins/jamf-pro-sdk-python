:tocdepth: 2

Classic API Models
==================

.. note::

    The intended use of SDK models is to provide an easier developer experience when working with
    requests and responses. All fields are optional, and extra fields are allowed for when Jamf
    releases a new version that adds additional fields that are not yet reflected in the SDK. These
    extra fields when present may or may not reflect their actual types. Do not rely solely on the
    SDK models for data validation.

Shared Models
-------------

.. currentmodule:: jamf_pro_sdk.models.classic

.. autosummary::
    :toctree: _autosummary

    ClassicApiModel
    ClassicDeviceLocation
    ClassicDevicePurchasing
    ClassicSite

Categories
----------

.. currentmodule:: jamf_pro_sdk.models.classic.categories

.. autosummary::
    :toctree: _autosummary

    ClassicCategory
    ClassicCategoriesItem

Computers
---------

.. currentmodule:: jamf_pro_sdk.models.classic.computers

.. autosummary::
    :toctree: _autosummary

    ClassicComputer
    ClassicComputersItem
    ClassicComputerGeneral
    ClassicComputerGeneralRemoteManagement
    ClassicComputerGeneralMdmCapableUsers
    ClassicComputerGeneralManagementStatus
    ClassicComputerHardware
    ClassicComputerHardwareStorageDevice
    ClassicComputerHardwareStorageDevicePartition
    ClassicComputerHardwareMappedPrinter
    ClassicComputerCertificate
    ClassicComputerSecurity
    ClassicComputerSoftware
    ClassicComputerSoftwareItem
    ClassicComputerSoftwareAvailableUpdate
    ClassicComputerExtensionAttribute
    ClassicComputerGroupsAccounts
    ClassicComputerGroupsAccountsLocalAccount
    ClassicComputerGroupsAccountsUserInventories
    ClassicComputerGroupsAccountsUserInventoriesUser
    ClassicComputerConfigurationProfile

Computer Groups
---------------

.. currentmodule:: jamf_pro_sdk.models.classic.computer_groups

.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    ClassicComputerGroup
    ClassicComputerGroupMembershipUpdate
    ClassicComputerGroupMember
    ClassicComputerGroupCriterion
    ClassicComputerGroupCriterionSearchType

NetworkSegments
---------------

.. currentmodule:: jamf_pro_sdk.models.classic.network_segments

.. autosummary::
    :toctree: _autosummary

    ClassicNetworkSegment
    ClassicNetworkSegmentItem

Sites
-----

.. currentmodule:: jamf_pro_sdk.models.classic.sites

.. autosummary::
    :toctree: _autosummary

    ClassicSite
    ClassicSiteItem
