# Changelog

<!-- This file is to only be updated on version releases and not with feature/fix PRs. -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9a1] - 2026-05-07

This release replaces several Jamf Pro API endpoints that Jamf has deprecated or removed. All previous methods are preserved with `DeprecationWarning` notices, and new methods are added alongside them. No breaking changes. 

Big thanks to [@cr3ation](https://github.com/cr3ation) for driving the API endpoint refresh.

### Added

- v3 computer inventory endpoints: `get_computer_inventory_v3()`, `get_computer_inventory_detail_v3()`, `get_computer_v3()`, `update_computer_v3()`, `delete_computer_v3()`
- `send_mdm_commandv2()` plus ~25 new MDM command models (`DeviceLockCommand`, `DeviceInformationCommand`, `EnableRemoteDesktopCommand`, `SecurityInfoCommand`, etc.) and a shared `MdmCommand` base class for typed method signatures.
- Direct package upload via `upload_package_v1()` and `client.jcds2.upload_package()` -- no extra deps required
- `cfBundleShortVersionString` and `cfBundleVersion` fields on `ComputerApplication`.
- `lastInventoryUpdateDate` filter field for the mobile inventory API. 

### Changed

- `_request_access_token` method in `ApiClientCredentialsProvider` updated.

### Deprecated

- `get_computer_inventory_v1()` (Jamf deprecated 2025-06-30) - use `get_computer_inventory_v3()`.
- `send_mdm_command_preview()` (remove from Jamf API schema) - use `send_mdm_command_v2()`.
- `create_jcds_file_v1()` and `client.jcds2.upload_file()` (Jamf deprecated 2025-08-28) - use `upload_package_v1()` / `client.jcds2.upload_package()`.

### Fixed

- Typo in `api_options`: `serAndLocation.buildingId` → `userAndLocation.buildingId`. 

### PRs Included

- [#65](https://github.com/macadmins/jamf-pro-sdk-python/pull/65)
- [#66](https://github.com/macadmins/jamf-pro-sdk-python/pull/66)
- [#79](https://github.com/macadmins/jamf-pro-sdk-python/pull/79)

## [0.8a1] - 2025-05-19

This version includes **breaking changes** for credential providers. `BasicAuthCredentialProvider` has been deprecated and removed.
Please migrate to `ApiClientCredentialsProvider` if you haven't done so already. [Client credentials](https://developer.jamf.com/jamf-pro/docs/client-credentials) with API roles and clients is the recommended path forward.
Where basic auth is still required with username/password use `UserCredentialsProvider`. 

### Changed

- Update sort and filter fields for device inventory endpoints.
- Change default credential provider to `ApiClientCredentialsProvider` in docs.
- Refactored `LoadFromAWSSecretsManager`, `PromptForCredentials` and `LoadFromKeychain` into helper functions instead of classes. Each function returns a `CredentialProvider` type that is specified or raises a `TypeError` if an invalid credential provider was passed.

### Fixed

- GitHub Actions workflows now pin action versions to commit hash. Docs publishing was broken due to outdated actions.

### PRs Included

- [#57](https://github.com/macadmins/jamf-pro-sdk-python/pull/57)
- [#60](https://github.com/macadmins/jamf-pro-sdk-python/pull/60)
- [#62](https://github.com/macadmins/jamf-pro-sdk-python/pull/62)

## [0.7a1] - 2024-12-03

Special shoutout to [macserv](https://github.com/macserv) for this contribution to the project!

### Added

- Pro API `get_packages_v1()`

### Changed

- Overload interfaces for Pro API methods that have multiple return types (this will now be a standard going forward).
- Added `files` argument for `pro_api_request()` to pass through to `requests` for `POST` requests.

### Fixed

- Various Python typing enhancements.

### PRs Included

- [#54](https://github.com/macadmins/jamf-pro-sdk-python/pull/54)

## [0.6a2] - 2024-07-24

### Changed

- Fixed missing criteria options for Classic API advanced searches and groups.
- Fixed sections not being passed when calling `get_mobile_device_inventory_v2()`.
- Fix malformed XML when generating computer group data from a model.
- Removed `black` from dev tools.

### PRs Included

- [#42](https://github.com/macadmins/jamf-pro-sdk-python/pull/42)
- [#45](https://github.com/macadmins/jamf-pro-sdk-python/pull/45)
- [#48](https://github.com/macadmins/jamf-pro-sdk-python/pull/48)
- [#49](https://github.com/macadmins/jamf-pro-sdk-python/pull/49)
- [#50](https://github.com/macadmins/jamf-pro-sdk-python/pull/50)

## [0.6a1] - 2024-02-13

### Added

- Pro API `get_mobile_device_inventory_v2()`

### Changed

- Added `end_page` argument to `get_mdm_commands_v2()`

### PRs Included

- [#39](https://github.com/macadmins/jamf-pro-sdk-python/pull/39)

## [0.5a2] - 2024-01-09

### Fixed

- V1Site model optional values did not have default of `None`.

## [0.5a1] - 2024-01-04

### Added

- Classic API `update_category_by_id()`
- Classic API `delete_category_by_id()`
- Classic API `create_category()`

### Changed

- Pydantic V2 Update

### Fixed

- Pagination bug with Pro API paginator.

### PRs Included

- [#26](https://github.com/macadmins/jamf-pro-sdk-python/pull/26)
- [#36](https://github.com/macadmins/jamf-pro-sdk-python/pull/36)

## [0.4a1] - 2023-10-25

### Added

- Classic API `create_advanced_computer_search()`
- Classic API `list_all_advanced_computer_searches()`
- Classic API `get_advanced_computer_search_by_id()`
- Classic API `update_advanced_computer_search_by_id()`
- Classic API `delete_advanced_computer_search_by_id()`
- Classic API `list_all_categories()`
- Classic API `get_category_by_id()`
- Classic API `set_computer_unmanaged_by_id()`
- Classic API `set_computer_managed_by_id()`

### PRs Included

- [#15](https://github.com/macadmins/jamf-pro-sdk-python/pull/15)
- [#20](https://github.com/macadmins/jamf-pro-sdk-python/pull/20)
- [#21](https://github.com/macadmins/jamf-pro-sdk-python/pull/21)
- [#22](https://github.com/macadmins/jamf-pro-sdk-python/pull/22)
