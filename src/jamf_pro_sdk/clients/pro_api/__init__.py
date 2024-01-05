from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterator, List, Union
from uuid import UUID

from ...models.pro.api_options import *  # noqa: F403
from ...models.pro.computers import Computer
from ...models.pro.jcds2 import DownloadUrl, File, NewFile
from ...models.pro.mdm import (
    CustomCommand,
    EnableLostModeCommand,
    EraseDeviceCommand,
    LogOutUserCommand,
    MdmCommandStatus,
    RenewMdmProfileResponse,
    RestartDeviceCommand,
    SendMdmCommand,
    SendMdmCommandClientData,
    SendMdmCommandResponse,
    SetRecoveryLockCommand,
    ShutDownDeviceCommand,
)
from ...models.pro.scripts import *

from .pagination import Paginator

if TYPE_CHECKING:
    import requests

    from .pagination import FilterExpression, Page, SortExpression


class ProApi:
    """Provides an interface to the Jamf Pro API."""

    def __init__(
        self,
        request_method: Callable[..., requests.Response],
        concurrent_requests_method: Callable[..., Iterator],
    ):
        self.api_request = request_method
        self.concurrent_api_requests = concurrent_requests_method

    # Computer Inventory APIs

    def get_computer_inventory_v1(
        self,
        sections: List[str] = None,
        start_page: int = 0,
        end_page: int = None,
        page_size: int = 100,
        sort_expression: SortExpression = None,
        filter_expression: FilterExpression = None,
        return_generator: bool = False,
    ) -> Union[List[Computer], Iterator[Page]]:
        """Returns a list of computer inventory records.

        :param sections: (optional) Select which sections of the computer's details to return. If
            not specific the request will default to ``GENERAL``. If ``ALL`` is passed then all
            sections will be returned.

            Allowed sections:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_computer_inventory_v1_allowed_sections

        :type sections: List[str]

        :param start_page: (optional) The page to begin returning results from. See
            :class:`Paginator` for more information.
        :type start_page: int

        :param end_page: (optional) The page to end returning results at. See :class:`Paginator` for
            more information.
        :type start_page: int

        :param page_size: (optional) The number of results to include in each requested page. See
            :class:`Paginator` for more information.
        :type page_size: int

        :param sort_expression: (optional) The sort fields to apply to the request. See the
            documentation for :ref:`Pro API Sorting` for more information.

            Allowed sort fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_computer_inventory_v1_allowed_sort_fields

        :type sort_expression: SortExpression

        :param filter_expression: (optional) The filter expression to apply to the request. See the
            documentation for :ref:`Pro API Filtering` for more information.

            Allowed filter fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_computer_inventory_v1_allowed_filter_fields

        :type filter_expression: FilterExpression

        :param return_generator: If ``True`` a generator is returned to iterate over pages. By
            default, the results for all pages will be returned in a single response.
        :type return_generator: bool

        :return: List of computers OR a paginator generator.
        :rtype: List[~jamf_pro_sdk.models.pro.computer.Computer] | Iterator[Page]

        """
        if not sections:
            sections = ["GENERAL"]
        elif "ALL" in sections:
            sections = get_computer_inventory_v1_allowed_sections[1:]

        if not all([i in get_computer_inventory_v1_allowed_sections for i in sections]):
            raise ValueError(
                f"Values for 'sections' must be one of: {', '.join(get_computer_inventory_v1_allowed_sections)}"
            )

        if sort_expression:
            sort_expression.validate(get_computer_inventory_v1_allowed_sort_fields)

        if filter_expression:
            filter_expression.validate(get_computer_inventory_v1_allowed_filter_fields)

        paginator = Paginator(
            api_client=self,
            resource_path="v1/computers-inventory",
            return_model=Computer,
            start_page=start_page,
            end_page=end_page,
            page_size=page_size,
            sort_expression=sort_expression,
            filter_expression=filter_expression,
            extra_params={"section": ",".join(sections)},
        )

        return paginator(return_generator=return_generator)

    # JCDS APIs

    def get_jcds_files_v1(self) -> List[File]:
        """Return a list of files in the JCDS.

        :return: List JCDS File objects.
        :rtype: List[File]

        """
        resp = self.api_request(method="get", resource_path="v1/jcds/files")
        return [File(**i) for i in resp.json()]

    def create_jcds_file_v1(self) -> NewFile:
        """Create a new file in the JCDS.

        :return: A JCDS NewFile object.
        :rtype: NewFile

        """
        resp = self.api_request(method="post", resource_path="v1/jcds/files")
        return NewFile(**resp.json())

    def get_jcds_file_v1(self, file_name: str) -> DownloadUrl:
        """Read a JCDS file record by its filename.

        :return: A JCDS DownloadUrl object.
        :rtype: DownloadUrl

        """
        resp = self.api_request(method="get", resource_path=f"v1/jcds/files/{file_name}")
        return DownloadUrl(**resp.json())

    def delete_jcds_file_v1(self, file_name: str) -> None:
        """Delete a file from the JCDS.

        .. warning::

            This operation *WILL NOT* delete an associated package object. It is recommended to use
            :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.delete_package_by_id`.

        """
        self.api_request(method="delete", resource_path=f"v1/jcds/files/{file_name}")

    # MDM APIs

    def renew_mdm_profile_v1(self, udids: List[Union[str, UUID]]) -> RenewMdmProfileResponse:
        """Renews device MDM Profiles, including the device identity certificate within the MDM Profile.

        :param udids: A list of device UDIDs to issue the profile renewal action to.
        :type udids: List[str, UUID]

        :return: The ``RenewMdmProfileResponse`` returned may or may not contain a UDIDs not
            processed for renewal.
        :rtype: RenewMdmProfileResponse
        """
        resp = self.api_request(
            method="post",
            resource_path="v1/mdm/renew-profile",
            data={"udids": [str(i) for i in udids]},
        )

        try:
            return RenewMdmProfileResponse(
                udidsNotProcessed=resp.json()["udidsNotProcessed"]["udids"]
            )
        except KeyError:
            return RenewMdmProfileResponse(udidsNotProcessed=[])

    def send_mdm_command_preview(
        self,
        management_ids: List[Union[str, UUID]],
        command: Union[
            EnableLostModeCommand,
            EraseDeviceCommand,
            LogOutUserCommand,
            RestartDeviceCommand,
            SetRecoveryLockCommand,
            ShutDownDeviceCommand,
            CustomCommand,
        ],
    ) -> List[SendMdmCommandResponse]:
        """Send an MDM command to one or more devices.

        .. caution::

            This API is labeled as a **Preview** by Jamf. It may change or become deprecated in
            favor of another API in a future release.

        Example usage:

        .. code-block:: python

            from jamf_pro_sdk.models.pro.mdm import LogOutUserCommand

            client.pro_api.send_mdm_command_preview(
                management_ids=["4eecc1fb-f52d-48c5-9560-c246b23601d3"],
                command=LogOutUserCommand()
            )

        Read the documentation for :ref:`MDM Command Models` to view all the options for the
        supported MDM commands . The management IDs can be obtained from computer inventory records
        at ``computer.general.managementId``.

        This value is only available through the Pro API. See
        :class:`~jamf_pro_sdk.models.pro.computers.ComputerGeneral` for more details.

        :param management_ids: A list of device management IDs to issue the MDM command to.
        :type management_ids: List[Union[str, UUID]],

        :param command: The MDM command to send.
        :type command: Union[EnableLostModeCommand, EraseDeviceCommand, RestartDeviceCommand,
            ShutDownDeviceCommand, CustomCommand]

        :return: A list of command responses.
        :rtype: List[SendMdmCommandResponse]
        """
        data = SendMdmCommand(
            clientData=[SendMdmCommandClientData(managementId=i) for i in management_ids],
            commandData=command,
        )

        resp = self.api_request(method="post", resource_path="preview/mdm/commands", data=data)
        return [SendMdmCommandResponse(**i) for i in resp.json()]

    def get_mdm_commands_v2(
        self,
        filter_expression: FilterExpression,
        start_page: int = 0,
        page_size: int = 100,
        sort_expression: SortExpression = None,
        return_generator: bool = False,
    ) -> Union[List[MdmCommandStatus], Iterator[Page]]:
        """Returns a list of MDM commands.

        :param filter_expression: The filter expression to apply to the request. At least **one**
            filter is required for this operation. See the documentation for
            :ref:`Pro API Filtering` for more information.

            Allowed filter fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_mdm_commands_v2_allowed_filter_fields

        :type filter_expression: FilterExpression

        :param start_page: (optional) The page to begin returning results from. See
            :class:`Paginator` for more information.
        :type start_page: int

        :param page_size: (optional) The number of results to include in each requested page. See
            :class:`Paginator` for more information.
        :type page_size: int

        :param sort_expression: (optional) The sort fields to apply to the request. See the
            documentation for :ref:`Pro API Sorting` for more information.

            Allowed sort fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_mdm_commands_v2_allowed_sort_fields

        :type sort_expression: SortExpression

        :param return_generator: If ``True`` an iterator is returned that yields pages. By default,
            the results for all pages will be returned in a single response.
        :type return_generator: bool

        :return: List of computers OR a paginator generator.
        :rtype: List[~jamf_pro_sdk.models.pro.mdm.MdmCommand] | Iterator[Page]
        """

        if command_filters := [i for i in filter_expression.fields if i.name == "command"]:
            if not all(
                [i.value in get_mdm_commands_v2_allowed_command_types for i in command_filters]
            ):
                raise ValueError(
                    f"Values for 'command' filters must be one of: {', '.join(get_mdm_commands_v2_allowed_command_types)}"
                )

        if sort_expression:
            sort_expression.validate(get_mdm_commands_v2_allowed_sort_fields)

        if filter_expression:
            filter_expression.validate(get_mdm_commands_v2_allowed_filter_fields)

        paginator = Paginator(
            api_client=self,
            resource_path="v2/mdm/commands",
            return_model=MdmCommandStatus,
            start_page=start_page,
            page_size=page_size,
            sort_expression=sort_expression,
            filter_expression=filter_expression,
        )

        return paginator(return_generator=return_generator)

    def get_scripts_v1(
        self,
        start_page: int = 0,
        end_page: int = None,
        page_size: int = 100,
        sort_expression: SortExpression = None,
        filter_expression: FilterExpression = None,
        return_generator: bool = False,
    ) -> Union[List[Script], Iterator[Page]]:
        """Returns a list of script records.

                :param start_page: (optional) The page to begin returning results from. See
            :class:`Paginator` for more information.
        :type start_page: int

        :param end_page: (optional) The page to end returning results at. See :class:`Paginator` for
            more information.
        :type start_page: int

        :param page_size: (optional) The number of results to include in each requested page. See
            :class:`Paginator` for more information.
        :type page_size: int

        :param sort_expression: (optional) The sort fields to apply to the request. See the
            documentation for :ref:`Pro API Sorting` for more information.

            Allowed sort fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_scripts_v1_allowed_sort_criteria

        :type sort_expression: SortExpression

        :param filter_expression: (optional) The filter expression to apply to the request. See the
            documentation for :ref:`Pro API Filtering` for more information.

            Allowed filter fields:

            .. autoapioptions:: jamf_pro_sdk.models.pro.api_options.get_scripts_inventory_v1_allowed_filter_criteriascripts

        :type filter_expression: FilterExpression

        :param return_generator: If ``True`` a generator is returned to iterate over pages. By
            default, the results for all pages will be returned in a single response.
        :type return_generator: bool

        :return: List of scripts OR a paginator generator.
        :rtype: List[~jamf_pro_sdk.models.pro.script.Script] | Iterator[Page]
        """
        if sort_expression:
            sort_expression.validate(get_scripts_v1_allowed_sort_fields)

        if filter_expression:
            filter_expression.validate(get_scripts_v1_allowed_filter_fields)

        paginator = Paginator(
            api_client=self,
            resource_path="v1/scripts",
            return_model=Script,
            start_page=start_page,
            end_page=end_page,
            page_size=page_size,
            sort_expression=sort_expression,
            filter_expression=filter_expression,
        )

        return paginator(return_generator=return_generator)

    def get_script_v1(self, script_id: int) -> Script:
        """Returns a script record.

        :param script_id: The ID of the script to return.
        :type script_id: int

        :return: A script record.
        :rtype: ~jamf_pro_sdk.models.pro.script.Script
        """
        resp = self.api_request(method="get", resource_path=f"v1/scripts/id/{script_id}")
        return Script(**resp.json())

    def set_script(self, script_id: int, script: Script) -> Script:
        """Updates or creates a script record.

        :param script_id: The ID of the script to update.
        :type script_id: int

        :param script: The script record to update.
        :type script: ~jamf_pro_sdk.models.pro.script.Script

        :return: The updated script record.
        :rtype: ~jamf_pro_sdk.models.pro.script.Script
        """
        resp = self.api_request(
            method="put", resource_path=f"v1/scripts/id/{script_id}", data=script
        )
        return Script(**resp.json())

    def delete_script(self, script_id: int) -> None:
        """Deletes a script record.

        :param script_id: The ID of the script to delete.
        :type script_id: int
        """
        self.api_request(method="delete", resource_path=f"v1/scripts/id/{script_id}")

    def create_script(self, script: Script) -> Script:
        """Creates a script record.

        :param script: The script record to create.
        :type script: ~jamf_pro_sdk.models.pro.script.Script

        :return: The created script record.
        :rtype: ~jamf_pro_sdk.models.pro.script.Script
        """
        resp = self.api_request(method="post", resource_path="v1/scripts", data=script)
        return Script(**resp.json())
