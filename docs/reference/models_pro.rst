:tocdepth: 2

Pro API Models
==============

.. note::

    The intended use of SDK models is to provide an easier developer experience when working with
    requests and responses. All fields are optional, and extra fields are allowed for when Jamf
    releases a new version that adds additional fields that are not yet reflected in the SDK. These
    extra fields when present may or may not reflect their actual types. Do not rely solely on the
    SDK models for data validation.

Computers
---------

.. currentmodule:: jamf_pro_sdk.models.pro.computers

.. autosummary::
    :toctree: _autosummary

    Computer
    ComputerGeneral
    ComputerDiskEncryption
    ComputerPurchase
    ComputerApplication
    ComputerStorage
    ComputerUserAndLocation
    ComputerConfigurationProfile
    ComputerPrinter
    ComputerService
    ComputerHardware
    ComputerLocalUserAccount
    ComputerCertificate
    ComputerAttachment
    ComputerPlugin
    ComputerPackageReceipts
    ComputerFont
    ComputerSecurity
    ComputerOperatingSystem
    ComputerLicensedSoftware
    ComputeriBeacon
    ComputerSoftwareUpdate
    ComputerExtensionAttribute
    ComputerContentCaching
    ComputerGroupMembership

JCDS2
-----

.. currentmodule:: jamf_pro_sdk.models.pro.jcds2

.. autosummary::
    :toctree: _autosummary

    NewFile
    File
    DownloadUrl

.. _MDM Command Models:

MDM Commands
------------

.. currentmodule:: jamf_pro_sdk.models.pro.mdm

.. autosummary::
    :toctree: _autosummary

    SendMdmCommand
    SendMdmCommandClientData
    EnableLostModeCommand
    EraseDeviceCommand
    EraseDeviceCommandObliterationBehavior
    EraseDeviceCommandReturnToService
    LogOutUserCommand
    RestartDeviceCommand
    ShutDownDeviceCommand
    SendMdmCommandResponse
    RenewMdmProfileResponse
    MdmCommandStatus
    MdmCommandStatusClient
    MdmCommandStatusClientTypes
    MdmCommandStatusStates
    MdmCommandStatusTypes

Pagination
----------

.. currentmodule:: jamf_pro_sdk.clients.pro_api.pagination

.. autosummary::
    :toctree: _autosummary

    Page
    FilterEntry


Scripts
-------

.. currentmodule:: jamf_pro_sdk.models.pro.scripts

.. autosummary::
    :toctree: _autosummary

    Script
