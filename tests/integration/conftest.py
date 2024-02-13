import logging
import os

import pytest

from jamf_pro_sdk import (
    JamfProClient,
    SessionConfig,
    logger_quick_setup,
)
from jamf_pro_sdk.clients.auth import ApiClientCredentialsProvider

# https://developer.jamf.com/developer-guide/docs/populating-dummy-data
JAMF_PRO_HOST = os.getenv("JAMF_PRO_HOST")
JAMF_PRO_CLIENT_ID = os.getenv("JAMF_PRO_CLIENT_ID")
JAMF_PRO_CLIENT_SECRET = os.getenv("JAMF_PRO_CLIENT_SECRET")

# Run pytest with '-s' to view logging output
logger_quick_setup(logging.DEBUG)


@pytest.fixture(scope="module")
def jamf_client():
    client = JamfProClient(
        server=JAMF_PRO_HOST,
        credentials=ApiClientCredentialsProvider(
            client_id=JAMF_PRO_CLIENT_ID, client_secret=JAMF_PRO_CLIENT_SECRET
        ),
        session_config=SessionConfig(timeout=30),
    )

    # Retrieve an access token immediately after init
    client.get_access_token()

    return client
