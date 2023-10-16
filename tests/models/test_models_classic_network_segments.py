import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.classic.network_segments import ClassicNetworkSegment

NETWORK_SEGMENT_JSON = {
    "network_segment": {
        "id": 1,
        "name": "Test Network",
        "starting_address": "192.168.1.31",
        "ending_address": "192.168.7.255",
    }
}


def test_network_segment_model_parsings():
    """Verify select attributes across the NetworkSegment model."""
    network_segment = ClassicNetworkSegment(**NETWORK_SEGMENT_JSON["network_segment"])

    assert network_segment is not None  # mypy
    assert network_segment.name == "Test Network"
    assert network_segment.starting_address == "192.168.1.31"
    assert network_segment.ending_address == "192.168.7.255"
    assert network_segment.id == 1


def test_network_segment_model_json_output_matches_input():
    network_segment = ClassicNetworkSegment(**NETWORK_SEGMENT_JSON["network_segment"])
    serialized_output = json.loads(network_segment.json(exclude_none=True))

    diff = DeepDiff(NETWORK_SEGMENT_JSON["network_segment"], serialized_output, ignore_order=True)

    assert not diff
