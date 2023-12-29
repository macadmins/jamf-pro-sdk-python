import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.classic.network_segments import ClassicNetworkSegment

NETWORK_SEGMENT_JSON = {
    "network_segment": {
        "id": 1,
        "name": "Test Network",
        "starting_address": "192.168.1.31",
        "ending_address": "192.168.7.255",
        "distribution_point": "Cloud Distribution Point",
        "url": "https://use1-jcds.services.jamfcloud.com/download/66d8960449b44a668c38e4dddbe094d7",
        "building": "Test Building",
        "department": "Test Department",
    }
}


def test_network_segment_model_parsings():
    """Verify select attributes across the NetworkSegment model."""
    network_segment = ClassicNetworkSegment.model_validate(NETWORK_SEGMENT_JSON["network_segment"])

    assert network_segment is not None  # mypy
    assert network_segment.name == "Test Network"
    assert network_segment.starting_address == "192.168.1.31"
    assert network_segment.ending_address == "192.168.7.255"
    assert network_segment.id == 1
    assert network_segment.distribution_point == "Cloud Distribution Point"
    assert (
        network_segment.url
        == "https://use1-jcds.services.jamfcloud.com/download/66d8960449b44a668c38e4dddbe094d7"
    )
    assert network_segment.building == "Test Building"
    assert network_segment.department == "Test Department"


def test_network_segment_model_json_output_matches_input():
    network_segment = ClassicNetworkSegment.model_validate(NETWORK_SEGMENT_JSON["network_segment"])
    serialized_output = json.loads(network_segment.model_dump_json(exclude_none=True))

    diff = DeepDiff(NETWORK_SEGMENT_JSON["network_segment"], serialized_output, ignore_order=True)

    assert not diff
