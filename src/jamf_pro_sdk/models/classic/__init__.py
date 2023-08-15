from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Set

import dicttoxml
from pydantic import Extra

from .. import BaseModel


def convert_datetime_to_jamf_iso(dt: datetime) -> str:
    """Classic API deviates from the published Jamf API Style Guide:
    https://developer.jamf.com/developer-guide/docs/api-style-guide#date--time-format
    """
    if not dt.tzinfo:
        raise ValueError("Datetime object must have timezone information")

    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + dt.strftime("%z")


def remove_fields(data: Any, values_to_remove: Iterable = None):
    """For use with the .xml() method of the `ClassicApiModel`.

    When constructing resources using models and some default sub-models are instantiated
    for ease of developer use. Upon export to XML, any empty objects and arrays are removed
    to prevent overwriting existing data in the API.
    """
    if not values_to_remove:
        values_to_remove = [{}, []]

    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if v in values_to_remove:
                continue
            elif isinstance(v, dict):
                v = remove_fields(v, values_to_remove)
            elif isinstance(v, list):
                new_v = []
                for i in v:
                    print("Array item: ", i)
                    if new_i := remove_fields(i, values_to_remove):
                        new_v.append(new_i)
                v = new_v

            new_data[k] = v
        return new_data

    elif data not in values_to_remove:
        return data


class ClassicApiModel(BaseModel):
    """The base model used for Classic API models."""

    _xml_root_name: str
    _xml_array_item_names: Dict[str, str]
    _xml_write_fields: Optional[Set[str]] = None

    def xml(self, exclude_none: bool = True, exclude_read_only: bool = False) -> str:
        """Generate a Jamf Pro XML representation of the model.

        :param exclude_none: Any field with a value of ``None`` is not included.
        :type exclude_none: bool

        :param exclude_read_only: If write field names are set, only include those.
        :type exclude_read_only: bool

        :return: XML string
        :rtype: str
        """
        data = remove_fields(
            self.dict(
                include=self._xml_write_fields if exclude_read_only else None,
                exclude_none=exclude_none,
            )
        )

        return dicttoxml.dicttoxml(
            data,
            custom_root=self._xml_root_name,
            attr_type=False,
            item_func=self._xml_array_item_names.get,
            return_bytes=False,
        )

    class Config:
        extra = Extra.allow
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_jamf_iso
        }


class ClassicDeviceLocation(BaseModel):
    """Device user assignment information."""

    username: Optional[str]
    realname: Optional[str]
    real_name: Optional[str]
    email_address: Optional[str]
    position: Optional[str]
    phone: Optional[str]
    phone_number: Optional[str]
    department: Optional[str]
    building: Optional[str]
    room: Optional[str]


class ClassicDevicePurchasing(BaseModel):
    """Device purchase information (normally populated by GSX)."""

    is_purchased: Optional[bool]
    is_leased: Optional[bool]
    po_number: Optional[str]
    vendor: Optional[str]
    applecare_id: Optional[str]
    purchase_price: Optional[str]
    purchasing_account: Optional[str]
    po_date: Optional[str]
    po_date_epoch: Optional[int]
    po_date_utc: Optional[str]
    warranty_expires: Optional[str]
    warranty_expires_epoch: Optional[int]
    warranty_expires_utc: Optional[str]
    lease_expires: Optional[str]
    lease_expires_epoch: Optional[int]
    lease_expires_utc: Optional[str]
    life_expectancy: Optional[int]
    purchasing_contact: Optional[str]
    os_applecare_id: Optional[str]
    os_maintenance_expires: Optional[str]
    attachments: Optional[list]  # Deprecated?


class ClassicSite(BaseModel):
    """Site assignment information."""

    id: Optional[int]
    name: Optional[str]
