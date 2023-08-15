from datetime import datetime, timezone

from pytest import raises
from src.jamf_pro_sdk.models.classic import convert_datetime_to_jamf_iso, remove_fields


def test_convert_datetime_to_jamf_iso():
    dt = datetime(2023, 1, 1, 12, 30, 1, 321000, tzinfo=timezone.utc)
    assert convert_datetime_to_jamf_iso(dt) == "2023-01-01T12:30:01.321+0000"


def test_convert_datetime_to_jamf_iso_no_tz():
    dt = datetime(2023, 1, 1, 12, 30, 1, 321000)
    with raises(ValueError):
        convert_datetime_to_jamf_iso(dt)


def test_remove_fields():
    data = {
        "general": {"id": 123, "remote_management": {}},
        "location": {},
        "hardware": {
            "filevault2_users": ["admin"],
        },
        "extension_attributes": [{}, {"id": 1, "value": "foo"}],
        "certificates": [],
    }

    cleaned_data = remove_fields(data)

    assert cleaned_data == {
        "general": {"id": 123},
        "hardware": {
            "filevault2_users": ["admin"],
        },
        "extension_attributes": [{"id": 1, "value": "foo"}],
    }
