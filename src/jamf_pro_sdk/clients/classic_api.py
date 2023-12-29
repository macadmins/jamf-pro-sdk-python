from __future__ import annotations

import secrets
import string
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, List, Union

from defusedxml.ElementTree import fromstring

from ..models.classic.advanced_computer_searches import (
    ClassicAdvancedComputerSearch,
    ClassicAdvancedComputerSearchesItem,
)
from ..models.classic.categories import ClassicCategoriesItem, ClassicCategory
from ..models.classic.computer_groups import (
    ClassicComputerGroup,
    ClassicComputerGroupMember,
    ClassicComputerGroupMembershipUpdate,
)
from ..models.classic.computers import (
    ClassicComputer,
    ClassicComputersItem,
)
from ..models.classic.packages import ClassicPackage, ClassicPackageItem

if TYPE_CHECKING:
    import requests

VALID_COMPUTER_SUBSETS = (
    "general",
    "location",
    "purchasing",
    "peripherals",
    "hardware",
    "certificates",
    "software",
    "extensionattributes",
    "groupsaccounts",
    "configurationprofiles",
)  #: Valid subsets for the :meth:`~ClassicApi.list_computers` operation.

CategoryId = Union[int, ClassicCategory, ClassicCategoriesItem]
ComputerId = Union[int, ClassicComputer, ClassicComputersItem]
AdvancedComputerSearchId = Union[
    int, ClassicAdvancedComputerSearch, ClassicAdvancedComputerSearchesItem
]
PackageId = Union[int, ClassicPackage, ClassicPackageItem]


def parse_response_id(xml: str) -> int:
    """Returns the ``id`` value from an XML doc."""
    root = fromstring(xml)
    return int(root.find("id").text)


class ClassicApi:
    """Provides a curated interface to the Jamf Pro Classic API."""

    def __init__(
        self,
        request_method: Callable[..., requests.Response],
        concurrent_requests_method: Callable[..., Iterator],
    ):
        self.api_request = request_method
        self.concurrent_api_requests = concurrent_requests_method

    @staticmethod
    def _parse_id(model: Union[int, object]) -> int:
        """If the model has an ``id`` attribute return that value (most Classic API models have this
        as top-level field).If the model is a ``ClassicComputer`` return the nested value.
        """
        if hasattr(model, "id"):
            return model.id
        elif isinstance(model, ClassicComputer):
            return model.general.id
        else:
            return model

    # /categories APIs

    def list_all_categories(self) -> List[ClassicCategoriesItem]:
        """Returns a list of all categories.

        :return: List of categories.
        :rtype: List[ClassicCategoriesItem]

        """
        resp = self.api_request(method="get", resource_path="categories")
        return [ClassicCategoriesItem(**i) for i in resp.json()["categories"]]

    def get_category_by_id(self, category: CategoryId) -> ClassicCategory:
        """Returns a single category record using the ID.

        :param category: A category ID or supported Classic API model.
        :type category: Union[int, ClassicCategory, ClassicCategoriesItem]

        :return: Category.
        :rtype: ClassicCategory

        """
        category_id = ClassicApi._parse_id(category)
        resp = self.api_request(method="get", resource_path=f"categories/id/{category_id}")
        return ClassicCategory(**resp.json()["category"])

    def update_category_by_id(
        self, category: CategoryId, data: Union[str, ClassicCategory]
    ) -> None:
        """Update a single category record using the ID.

        :param category: A category ID or supported Classic API model.
        :type category: Union[int, ClassicCategory, ClassicCategoriesItem]

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.categories.ClassicCategory` object.
        :type data: Union[str, ClassicCategory]
        """
        category_id = ClassicApi._parse_id(category)
        self.api_request(method="put", resource_path=f"categories/id/{category_id}", data=data)

    def delete_category_by_id(self, category: CategoryId) -> None:
        """Delete a single category record using the ID.

        :param category: A category ID or supported Classic API model.
        :type category: Union[int, ClassicCategory, ClassicCategoriesItem]

        """
        category_id = ClassicApi._parse_id(category)
        self.api_request(method="delete", resource_path=f"categories/id/{category_id}")

    def create_category(self, data: Union[str, ClassicCategory]) -> int:
        """Create a new category.

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.categories.ClassicCategory` object.
        :type data: Union[str, ClassicCategory]

        :return: ID of the new category.
        :rtype: int

        """
        resp = self.api_request(method="post", resource_path="categories/id/0", data=data)
        return parse_response_id(resp.text)

    # /computers APIs

    def list_all_computers(self, subsets: Iterable[str] = None) -> List[ClassicComputersItem]:
        """Returns a list of all computers.

        :param subsets: (optional) This operations accepts the ``basic`` subset to return
            additional details for every computer record. No other subset values are
            supported.
        :type subsets: Iterable

        :return: List of computers.
        :rtype: List[~jamf_pro_sdk.models.classic.computers.ClassicComputersItem]

        """
        if subsets:
            if not all(i.lower() in ("basic",) for i in subsets):
                raise ValueError(f"Invalid subset(s). Must be one of: ('basic').")
            path = "computers/subset/basic"
        else:
            path = "computers"

        resp = self.api_request(method="get", resource_path=path)
        return [ClassicComputersItem(**i) for i in resp.json()["computers"]]

    def get_computer_by_id(
        self, computer: ComputerId, subsets: Iterable[str] = None
    ) -> ClassicComputer:
        """Returns a single computer record using the ID.

        :param computer: A computer ID or supported Classic API model.
        :type computer: Union[int, ClassicComputer, ClassicComputersItem]

        :param subsets: (optional) This operation accepts subset values to limit the
            details returned with the computer record. The following subset values are
            accepted: ``general``, ``location``, ``purchasing``, ``peripherals``,
            ``hardware``, ``certificates``, ``software``, ``extensionattributes``,
            ``groupsaccounts``, and ``configurationprofiles``.

        :return: Computer.
        :rtype: ~jamf_pro_sdk.models.classic.computers.ClassicComputer

        """
        computer_id = ClassicApi._parse_id(computer)
        if subsets:
            if not all(i.lower() in VALID_COMPUTER_SUBSETS for i in subsets):
                raise ValueError(f"Invalid subset(s). Must be one of: {VALID_COMPUTER_SUBSETS}.")
            path = f"computers/id/{computer_id}/subset/{'&'.join(subsets)}"
        else:
            path = f"computers/id/{computer_id}"

        resp = self.api_request(method="get", resource_path=path)
        return ClassicComputer(**resp.json()["computer"])

    def get_computers(
        self, computers: List[ComputerId] = None, subsets: Iterable[str] = None
    ) -> Iterator[ClassicComputer]:
        """Returns all requested computer records by their IDs. This is a wrapper to the concurrent
        API requests method. If ``computers`` is not provided a call to
        :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.list_all_computers` is made to obtain
        the full list of computer IDs.

        :param computers: (optional) A list of computer IDs or supported Classic API models.
        :type computers: List[Union[int, ClassicComputer, ClassicComputersItem]]

        :param subsets: (optional) This operation accepts subset values to limit the
            details returned with the computer record. The following subset values are
            accepted: ``general``, ``location``, ``purchasing``, ``peripherals``,
            ``hardware``, ``certificates``, ``software``, ``extensionattributes``,
            ``groupsaccounts``, and ``configurationprofiles``.

        :return: List of computers.
        :rtype: List[~jamf_pro_sdk.models.classic.computers.ClassicComputer]

        """
        if not computers:
            computers = self.list_all_computers()

        return self.concurrent_api_requests(
            self.get_computer_by_id, [{"computer": i, "subsets": subsets} for i in computers]
        )

    def update_computer_by_id(
        self, computer: ComputerId, data: Union[str, ClassicComputer]
    ) -> None:
        """Update a single computer record using the ID.

        .. important::

            Not all fields in a computer record can be updated.

        :param computer: A computer ID or supported Classic API model.
        :type computer: Union[int, ClassicComputer, ClassicComputersItem]

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.computers.ClassicComputer` object.
        :type data: Union[str, ~jamf_pro_sdk.models.classic.computers.Computer]

        """
        computer_id = ClassicApi._parse_id(computer)
        self.api_request(method="put", resource_path=f"computers/id/{computer_id}", data=data)

    def delete_computer_by_id(self, computer: ComputerId) -> None:
        """Delete a single computer record using the ID.

        :param computer: A computer ID or supported Classic API model.
        :type computer: Union[int, ClassicComputer, ClassicComputersItem]

        """
        computer_id = ClassicApi._parse_id(computer)
        self.api_request(method="delete", resource_path=f"computers/id/{computer_id}")

    def set_computer_unmanaged_by_id(self, computer: ComputerId) -> None:
        """Sets the management status to `unmanaged` for a single computer using the ID

        .. important::
            This action does not remove the management framework or mdm profile from the device

        :param computer: A computer ID or supported Classic API model.
        :type computer: Union[int,  ~jamf_pro_sdk.models.classic.computers.Computer, ComputersItem]
        """
        data = {
            "general": {
                "remote_management": {
                    "managed": False,
                    "management_username": "",
                    "management_password": "",
                }
            }
        }
        update_management = ClassicComputer(**data)
        computer_id = ClassicApi._parse_id(computer)
        self.api_request(
            method="put", resource_path=f"computers/id/{computer_id}", data=update_management
        )

    def set_computer_managed_by_id(
        self, computer: ComputerId, management_user: str = "admin", management_password: str = None
    ) -> None:
        """Sets the management status to `managed` for a single computer using the ID.

        .. important::
            The management user does not need to match any local user account but is required for the device to be "managed"

        :param computer: A computer ID or supported Classic API model.
        :type computer: Union[int, ~jamf_pro_sdk.models.classic.computers.Computer, ComputersItem]

        :param management_user: (optional) The management username. Defaults to 'admin' if not specified
        :type management_user: str

        :param management_password: (optional) The management password. Defaults to a randomly generated password if not specified
        :type management_password: str

        """
        if not management_password:
            management_password = "".join(
                secrets.choice(string.ascii_letters + string.punctuation) for _ in range(16)
            )
        computer_id = ClassicApi._parse_id(computer)

        data = {
            "general": {
                "remote_management": {
                    "managed": True,
                    "management_username": management_user,
                    "management_password": management_password,
                }
            }
        }
        manage_computer = ClassicComputer(**data)
        self.api_request(
            method="put", resource_path=f"computers/id/{computer_id}", data=manage_computer
        )

    # /computergroups APIs

    def create_computer_group(self, data: Union[str, ClassicComputerGroup]) -> int:
        """Create a new computer group.

        If you are creating a `STATIC` group you must set ``is_smart`` to ``False`` and
        cannot include any ``criteria``. You can include ``computers`` in your request to
        populate group member on creation.

        If you are creating a `SMART` group you must set ``is_smart`` to ``True`` and
        cannot include any ``computers``. If no ``criteria`` are included the new group
        will include all computers.

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.computer_groups.ClassicComputerGroup` object.
        :type data: Union[str, ClassicComputerGroup]

        :return: ID of the new computer group.
        :rtype: int

        """
        resp = self.api_request(method="post", resource_path="computergroups/id/0", data=data)
        return parse_response_id(resp.text)

    def list_all_computer_groups(self) -> List[ClassicComputerGroup]:
        """Returns a list of all computer groups.

        Only ``id``, ``name`` and ``is_smart`` are populated.

        :return: List of computer groups.
        :rtype: List[~jamf_pro_sdk.models.classic.computer_groups.ClassicComputerGroup]

        """
        resp = self.api_request(method="get", resource_path="computergroups")
        return [ClassicComputerGroup(**i) for i in resp.json()["computer_groups"]]

    def get_computer_group_by_id(self, computer_group_id: int) -> ClassicComputerGroup:
        """Returns a single computer group record using the ID.

        :param computer_group_id: The computer group ID.
        :type computer_group_id: int

        :return: Computer group.
        :rtype: ~jamf_pro_sdk.models.classic.computer_groups.ClassicComputerGroup

        """
        resp = self.api_request(
            method="get", resource_path=f"computergroups/id/{computer_group_id}"
        )
        return ClassicComputerGroup(**resp.json()["computer_group"])

    def update_smart_computer_group_by_id(
        self, computer_group_id: int, data: Union[str, ClassicComputerGroup]
    ):
        """Update a smart computer group.

        The ``is_smart`` field must be set to ``True`` on the computer group to use this
        operation.

        This operation will replace the current ``criteria`` for the group. It is
        recommended you get the current state, modify the ``criterion`` objects as
        needed, and pass them into a new ``ClassicComputerGroup`` object for the update.

        :param computer_group_id: The computer group ID.
        :type computer_group_id: int

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.computer_groups.ClassicComputerGroup` object.
        :type data: Union[str, ClassicComputerGroup]

        """
        self.api_request(
            method="put",
            resource_path=f"computergroups/id/{computer_group_id}",
            data=data,
        )

    def update_static_computer_group_membership_by_id(
        self,
        computer_group_id: int,
        computers_to_add: Iterable[Union[int, ClassicComputerGroupMember]] = None,
        computers_to_remove: Iterable[Union[int, ClassicComputerGroupMember]] = None,
    ) -> None:
        """Update the membership of a static computer group.

        The ``is_smart`` field must be set to ``False`` on the computer group to use this
        operation.

        :param computer_group_id: The computer group ID.
        :type computer_group_id: int

        :param computers_to_add: An array of computer IDs, or ``ClassicComputerGroupMember``
            objects to add to the static group.
        :type computers_to_add: Iterable[Union[int, ClassicComputerGroupMember]]

        :param computers_to_remove: An array of computer IDs, or ``ClassicComputerGroupMember``
            objects to remove from the static group.
        :type computers_to_remove: Iterable[Union[int, ClassicComputerGroupMember]]

        """
        group_update = ClassicComputerGroupMembershipUpdate()

        if computers_to_add:
            group_update.computer_additions = []
            for i in computers_to_add:
                group_update.computer_additions.append(
                    ClassicComputerGroupMember(id=i) if isinstance(i, int) else i
                )

        if computers_to_remove:
            group_update.computer_deletions = []
            for i in computers_to_remove:
                group_update.computer_deletions.append(
                    ClassicComputerGroupMember(id=i) if isinstance(i, int) else i
                )

        self.api_request(
            method="put",
            resource_path=f"computergroups/id/{computer_group_id}",
            data=group_update,
        )

    # /advancedcomputersearches APIs

    def create_advanced_computer_search(
        self, data: Union[str, ClassicAdvancedComputerSearch]
    ) -> int:
        """Create a new advanced computer search.

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.advanced_computer_searches.ClassicAdvancedComputerSearch`
            object.
        :type data: Union[str, ClassicAdvancedComputerSearch]

        :return: ID of the new computer group.
        :rtype: int

        """
        resp = self.api_request(method="post", resource_path="advancedcomputersearches", data=data)
        return parse_response_id(resp.text)

    def list_all_advanced_computer_searches(self) -> List[ClassicAdvancedComputerSearchesItem]:
        """Returns a list of all advanced computer searches.

        :return: List of advanced computer searches.
        :rtype: List[ClassicAdvancedComputerSearchesItem]

        """
        resp = self.api_request(method="get", resource_path="advancedcomputersearches")
        return [
            ClassicAdvancedComputerSearchesItem(**i)
            for i in resp.json()["advanced_computer_searches"]
        ]

    def get_advanced_computer_search_by_id(self, advanced_search: AdvancedComputerSearchId):
        """Returns a single advanced computer search using the ID.

        This operation returns the results of the advanced search when called. The ``computers``
        field will contain an array of the results with data fields matching those in the
        ``display_fields`` field.

        Results are calculated on each call to this operation.

        :param advanced_search: An advanced computer search ID or supported Classic API model.
        :type advanced_search: Union[int, ClassicAdvancedComputerSearch, ClassicAdvancedComputerSearchesItem]

        :return: Advanced computer search.
        :rtype: ~jamf_pro_sdk.models.classic.advanced_computer_searches.ClassicAdvancedComputerSearch

        """
        advanced_search_id = ClassicApi._parse_id(advanced_search)
        resp = self.api_request(
            method="get", resource_path=f"advancedcomputersearches/id/{advanced_search_id}"
        )
        return ClassicAdvancedComputerSearch(**resp.json()["advanced_computer_search"])

    def update_advanced_computer_search_by_id(
        self,
        advanced_search: AdvancedComputerSearchId,
        data: Union[str, ClassicAdvancedComputerSearch],
        return_updated: bool = False,
    ):
        """Update an advanced computer search using the ID.

        :param advanced_search: An advanced computer search ID or supported Classic API model.
        :type advanced_search: Union[int, ClassicAdvancedComputerSearch, ClassicAdvancedComputerSearchesItem]

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.advanced_computer_searches.ClassicAdvancedComputerSearch`
            object.
        :type data: Union[str, ClassicAdvancedComputerSearch]

        :param return_updated: If ``True`` the :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.get_advanced_computer_search_by_id`
            operation will be called after the update operation to return the updated results.
        :type return_updated: bool

        :return: Advanced computer search if ``return_updated`` is ``True``.
        :rtype: Union[None, ~jamf_pro_sdk.models.classic.advanced_computer_searches.ClassicAdvancedComputerSearch]

        """
        advanced_search_id = ClassicApi._parse_id(advanced_search)
        self.api_request(
            method="put",
            resource_path=f"advancedcomputersearches/id/{advanced_search_id}",
            data=data,
        )
        if return_updated:
            return self.get_advanced_computer_search_by_id(advanced_search_id)

    def delete_advanced_computer_search_by_id(self, advanced_search: AdvancedComputerSearchId):
        """Delete an advanced computer search using the ID.

        :param advanced_search: An advanced computer search ID or supported Classic API model.
        :type advanced_search: Union[int, ClassicAdvancedComputerSearch, ClassicAdvancedComputerSearchesItem]

        """
        advanced_search_id = ClassicApi._parse_id(advanced_search)
        self.api_request(
            method="delete",
            resource_path=f"advancedcomputersearches/id/{advanced_search_id}",
        )

    # /packages APIs

    def create_package(self, data: Union[str, ClassicPackage]) -> int:
        """Create a new package.

        Only the ``name`` and ``filename`` are required.
        Use with :meth:`~jamf_pro_sdk.clients.pro_api.ProApi.create_jcds_file_v1` to upload the
        package file to a Jamf Cloud Distribution Point.

        :param data: Can be an XML string or a
            :class:`~jamf_pro_sdk.models.classic.computer_groups.ClassicPackage` object.
        :type data: Union[str, ClassicPackage]

        :return: ID of the new package.
        :rtype: int

        """
        resp = self.api_request(method="post", resource_path="packages/id/0", data=data)
        return parse_response_id(resp.text)

    def list_all_packages(self) -> List[ClassicPackageItem]:
        """Returns a list of all packages.

        :return: List of packages.
        :rtype: List[~jamf_pro_sdk.models.classic.packages.ClassicPackageItem]

        """
        resp = self.api_request(method="get", resource_path="packages")
        return [ClassicPackageItem(**i) for i in resp.json()["packages"]]

    def get_package_by_id(self, package: PackageId) -> ClassicPackage:
        """Returns a single package record using the ID.

        :param package: A package ID or supported Classic API model.
        :type package: Union[int, ClassicPackage, ClassicPackageItem]

        :return: Package.
        :rtype: ~jamf_pro_sdk.models.classic.packages.ClassicPackage

        """
        package_id = ClassicApi._parse_id(package)
        resp = self.api_request(method="get", resource_path=f"packages/id/{package_id}")
        return ClassicPackage(**resp.json()["package"])

    def delete_package_by_id(self, package: PackageId) -> None:
        """Delete a single computer record using the ID.

        .. warning::

            This operation *WILL* delete an associated JCDS file.

        :param package: A package ID or supported Classic API model.
        :type package: Union[int, ClassicPackage, ClassicPackageItem]

        """
        package_id = ClassicApi._parse_id(package)
        self.api_request(method="delete", resource_path=f"packages/id/{package_id}")
