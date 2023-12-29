import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.classic.computer_groups import ClassicComputerGroup

COMPUTER_GROUP_JSON = {
    "computer_group": {
        "id": 1,
        "name": "All Managed Clients",
        "is_smart": True,
        "site": {"id": -1, "name": "None"},
        "criteria": [
            {
                "name": "Operating System",
                "priority": 0,
                "and_or": "and",
                "search_type": "not like",
                "value": "server",
                "opening_paren": False,
                "closing_paren": False,
            },
            {
                "name": "Application Title",
                "priority": 1,
                "and_or": "and",
                "search_type": "is not",
                "value": "Server.app",
                "opening_paren": False,
                "closing_paren": False,
            },
        ],
        "computers": [
            {
                "id": 123,
                "name": "Peccy's MacBook Pro",
                "mac_address": "AA:BB:CC:DD:EE:FF",
                "alt_mac_address": "",
                "serial_number": "C02XXXXXXHD1",
            },
            {
                "id": 456,
                "name": "Jeff's MacBook Pro",
                "mac_address": "00:11:22:33:44:55",
                "alt_mac_address": "",
                "serial_number": "C02XXXXXXHD2",
            },
        ],
    }
}


def test_computer_group_model_parsing():
    """Verify select attributes across the ComputerGroup model."""
    group = ClassicComputerGroup.model_validate(COMPUTER_GROUP_JSON["computer_group"])

    assert group is not None  # mypy
    assert group.criteria is not None  # mypy
    assert group.computers is not None  # mypy

    assert group.id == 1
    assert group.is_smart is True

    assert len(group.criteria) == 2
    assert len(group.computers) == 2

    assert group.criteria[0].name == "Operating System"
    assert group.criteria[0].search_type == "not like"
    assert group.criteria[0].value == "server"

    assert group.criteria[1].priority == 1
    assert group.criteria[1].and_or == "and"
    assert group.criteria[1].opening_paren is False

    assert group.computers[0].id == 123
    assert group.computers[0].name == "Peccy's MacBook Pro"

    assert group.computers[1].id == 456
    assert group.computers[1].mac_address == "00:11:22:33:44:55"


def test_computer_model_json_output_matches_input():
    computer = ClassicComputerGroup.model_validate(COMPUTER_GROUP_JSON["computer_group"])
    serialized_output = json.loads(computer.model_dump_json(exclude_none=True))

    diff = DeepDiff(COMPUTER_GROUP_JSON["computer_group"], serialized_output, ignore_order=True)

    assert not diff
