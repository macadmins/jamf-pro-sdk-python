from jamf_pro_sdk.models.client import AccessToken


def test_integration_basic_auth(jamf_client):
    current_token = jamf_client.get_access_token()
    assert isinstance(current_token, AccessToken)
    assert not current_token.is_expired
