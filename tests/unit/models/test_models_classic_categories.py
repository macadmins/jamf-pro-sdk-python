import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.classic.categories import ClassicCategory

CATEGORY_JSON = {"category": {"id": 1, "name": "Test Category", "priority": 1}}


def test_category_model_parsings():
    """Verify select attributes across the ComputerGroup model."""
    category = ClassicCategory.model_validate(CATEGORY_JSON["category"])

    assert category is not None  # mypy
    assert category.name == "Test Category"
    assert category.priority == 1
    assert category.id == 1


def test_category_model_json_output_matches_input():
    category = ClassicCategory.model_validate(CATEGORY_JSON["category"])
    serialized_output = json.loads(category.model_dump_json(exclude_none=True))

    diff = DeepDiff(CATEGORY_JSON["category"], serialized_output, ignore_order=True)

    assert not diff
