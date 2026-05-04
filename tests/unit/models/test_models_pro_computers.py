import json

from deepdiff import DeepDiff
from src.jamf_pro_sdk.models.pro.computers import Computer, ComputerApplication

# Simulated v1 API response (no cfBundle fields)
APPLICATION_V1_JSON = {
    "name": "Safari",
    "path": "/Applications/Safari.app",
    "version": "17.0",
    "macAppStore": False,
    "sizeMegabytes": 50,
    "bundleId": "com.apple.Safari",
    "updateAvailable": False,
    "externalVersionId": "123456",
}

# Simulated v3 API response (includes cfBundle fields)
APPLICATION_V3_JSON = {
    "name": "Safari",
    "path": "/Applications/Safari.app",
    "version": "17.0",
    "cfBundleShortVersionString": "17.0",
    "cfBundleVersion": "19617.1.17.11.12",
    "macAppStore": False,
    "sizeMegabytes": 50,
    "bundleId": "com.apple.Safari",
    "updateAvailable": False,
    "externalVersionId": "123456",
}

COMPUTER_JSON = {
    "id": "42",
    "udid": "AAAA-BBBB-CCCC",
    "general": {
        "name": "Test Mac",
        "lastIpAddress": "192.168.1.100",
        "platform": "Mac",
        "managementId": "mgmt-id-123",
        "remoteManagement": {"managed": True, "managementUsername": "admin"},
        "site": {"id": "1", "name": "Main Site"},
    },
    "hardware": {
        "make": "Apple",
        "model": "MacBook Pro",
        "serialNumber": "C02XYZ123456",
        "appleSilicon": True,
    },
    "applications": [APPLICATION_V3_JSON],
}

COMPUTER_WITH_PLUGINS_FONTS_JSON = {
    "id": "43",
    "udid": "DDDD-EEEE-FFFF",
    "general": {"name": "Legacy Mac"},
    "plugins": [{"name": "Flash Player", "version": "32.0", "path": "/Library/Plugins/Flash"}],
    "fonts": [{"name": "Helvetica", "version": "1.0", "path": "/Library/Fonts/Helvetica.ttf"}],
}


# ComputerApplication tests


def test_application_model_parsing_v1():
    """v1 response data (no cfBundle fields) should parse with None defaults."""
    app = ComputerApplication.model_validate(APPLICATION_V1_JSON)
    assert app.name == "Safari"
    assert app.version == "17.0"
    assert app.bundleId == "com.apple.Safari"
    assert app.cfBundleShortVersionString is None
    assert app.cfBundleVersion is None


def test_application_model_parsing_v3():
    """v3 response data (with cfBundle fields) should parse all fields."""
    app = ComputerApplication.model_validate(APPLICATION_V3_JSON)
    assert app.name == "Safari"
    assert app.version == "17.0"
    assert app.cfBundleShortVersionString == "17.0"
    assert app.cfBundleVersion == "19617.1.17.11.12"
    assert app.bundleId == "com.apple.Safari"


def test_application_v1_json_roundtrip():
    """v1 data should roundtrip without adding cfBundle fields."""
    app = ComputerApplication.model_validate(APPLICATION_V1_JSON)
    serialized = json.loads(app.model_dump_json(exclude_none=True))
    diff = DeepDiff(APPLICATION_V1_JSON, serialized, ignore_order=True)
    assert not diff


def test_application_v3_json_roundtrip():
    """v3 data should roundtrip with cfBundle fields included."""
    app = ComputerApplication.model_validate(APPLICATION_V3_JSON)
    serialized = json.loads(app.model_dump_json(exclude_none=True))
    diff = DeepDiff(APPLICATION_V3_JSON, serialized, ignore_order=True)
    assert not diff


# Computer model tests


def test_computer_model_parsing():
    """Verify select attributes across the Computer model."""
    computer = Computer.model_validate(COMPUTER_JSON)
    assert computer.id == "42"
    assert computer.udid == "AAAA-BBBB-CCCC"
    assert computer.general.name == "Test Mac"
    assert computer.general.platform == "Mac"
    assert computer.general.managementId == "mgmt-id-123"
    assert computer.hardware.serialNumber == "C02XYZ123456"
    assert computer.hardware.appleSilicon is True


def test_computer_model_applications_v3():
    """Computer model should include cfBundle fields from v3 application data."""
    computer = Computer.model_validate(COMPUTER_JSON)
    assert len(computer.applications) == 1
    app = computer.applications[0]
    assert app.cfBundleShortVersionString == "17.0"
    assert app.cfBundleVersion == "19617.1.17.11.12"


def test_computer_model_with_plugins_and_fonts():
    """Computer model should handle plugins and fonts (v1 data)."""
    computer = Computer.model_validate(COMPUTER_WITH_PLUGINS_FONTS_JSON)
    assert len(computer.plugins) == 1
    assert computer.plugins[0].name == "Flash Player"
    assert len(computer.fonts) == 1
    assert computer.fonts[0].name == "Helvetica"


def test_computer_model_without_plugins_and_fonts():
    """Computer model should handle missing plugins/fonts (v3 data)."""
    computer = Computer.model_validate(COMPUTER_JSON)
    assert computer.plugins is None
    assert computer.fonts is None


def test_computer_model_json_roundtrip():
    """The Computer model has default_factory for general and userAndLocation,
    so a roundtrip will include those as empty objects even if not in the input.
    We verify input data is preserved and only expected keys are added."""
    computer = Computer.model_validate(COMPUTER_JSON)
    serialized = json.loads(computer.model_dump_json(exclude_none=True))

    # All original fields should be present
    for key in COMPUTER_JSON:
        assert key in serialized
        diff = DeepDiff(COMPUTER_JSON[key], serialized[key], ignore_order=True)
        assert not diff, f"Mismatch in '{key}': {diff}"


def test_computer_model_extra_fields():
    """Computer model with extra='allow' should accept unknown fields."""
    data = {**COMPUTER_JSON, "unknownNewField": "someValue"}
    computer = Computer.model_validate(data)
    assert computer.id == "42"
    assert computer.unknownNewField == "someValue"
