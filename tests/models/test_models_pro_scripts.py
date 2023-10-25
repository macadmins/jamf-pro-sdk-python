import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.pro.scripts import Script

SCRIPT_JSON = {
    "script": {
        "id": 73,
        "name": "1_Set_Organization_Priorities-1.0.2.sh",
        "info": "Some information",
        "notes": "v1.0.2 31/1/2019",
        "priority": "AFTER",
        "parameter4": "",
        "parameter5": "",
        "parameter6": "",
        "parameter7": "",
        "parameter8": "",
        "parameter9": "",
        "parameter10": "",
        "parameter11": "",
        "osRequirements": "",
        "scriptContents": '#!/bin/bash\n\norganization="My Organization"',
        "categoryId": 15,
        "categoryName": "CIS",
    }
}


def test_script_model_parsings():
    """Verify select attributes across the Script model."""
    script = Script(**SCRIPT_JSON["script"])

    assert script is not None  # mypy
    assert script.id == 73
    assert script.name == "1_Set_Organization_Priorities-1.0.2.sh"
    assert script.info == "Some information"
    assert script.notes == "v1.0.2 31/1/2019"
    assert script.priority == "AFTER"
    assert script.parameter4 == ""
    assert script.parameter5 == ""
    assert script.parameter6 == ""
    assert script.parameter7 == ""
    assert script.parameter8 == ""
    assert script.parameter9 == ""
    assert script.parameter10 == ""
    assert script.parameter11 == ""
    assert script.scriptContents == '#!/bin/bash\n\norganization="My Organization"'
    assert script.categoryId == 15
    assert script.categoryName == "CIS"


def test_script_json_output_matches_input():
    script = Script(**SCRIPT_JSON["script"])
    serialized_output = json.loads(script.json(exclude_none=True))

    diff = DeepDiff(SCRIPT_JSON["script"], serialized_output, ignore_order=True)

    assert not diff
