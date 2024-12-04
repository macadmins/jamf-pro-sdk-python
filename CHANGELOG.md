# Changelog

<!-- This file is to only be updated on version releases and not with feature/fix PRs. -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
