import logging

import pytest

from jamf_pro_sdk import (
    JamfProClient,
    BasicAuthProvider,
    SessionConfig,
    logger_quick_setup,
)

JAMF_PRO_HOST = "dummy.jamfcloud.com"
JAMF_PRO_USERNAME = "demo"
JAMF_PRO_PASS = "tryitout"

logger_quick_setup(logging.DEBUG)


@pytest.fixture(scope="module")
def jamf_client():
    client = JamfProClient(
        server=JAMF_PRO_HOST,
        credentials=BasicAuthProvider(
            username=JAMF_PRO_USERNAME, password=JAMF_PRO_PASS
        ),
        session_config=SessionConfig(timeout=30),
    )

    # Retrieve an access token immediately after init
    client.get_access_token()

    return client
