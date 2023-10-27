import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.classic.sites import ClassicSite

SITE_JSON = {"site": {"id": 1, "name": "Test Site"}}


def test_site_model_parsings():
    """Verify select attributes across the Site model."""
    site = ClassicSite(**SITE_JSON["site"])

    assert site is not None  # mypy
    assert site.name == "Test Site"
    assert site.id == 1


def test_site_model_json_output_matches_input():
    site = ClassicSite(**SITE_JSON["site"])
    serialized_output = json.loads(site.json(exclude_none=True))

    diff = DeepDiff(SITE_JSON["site"], serialized_output, ignore_order=True)

    assert not diff
