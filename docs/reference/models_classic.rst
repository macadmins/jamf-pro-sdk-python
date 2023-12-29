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

Advanced Computer Searches
--------------------------

.. currentmodule:: jamf_pro_sdk.models.classic.advanced_computer_searches

.. autosummary::
    :toctree: _autosummary

    ClassicAdvancedComputerSearch
    ClassicAdvancedComputerSearchesItem
    ClassicAdvancedComputerSearchResult
    ClassicAdvancedComputerSearchDisplayField

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
    ClassicComputerGroupMember
    ClassicComputerGroupMembershipUpdate

Network Segments
----------------

.. currentmodule:: jamf_pro_sdk.models.classic.network_segments

.. autosummary::
    :toctree: _autosummary

    ClassicNetworkSegment
    ClassicNetworkSegmentItem

Packages
--------

.. currentmodule:: jamf_pro_sdk.models.classic.packages

.. autosummary::
    :toctree: _autosummary

    ClassicPackage
    ClassicPackageItem

Group and Search Criteria
-------------------------

.. currentmodule:: jamf_pro_sdk.models.classic.criteria

.. autosummary::
    :toctree: _autosummary

    ClassicCriterion
    ClassicCriterionSearchType
