class JamfProSdkException(Exception):
    """Base Jamf Pro SDK Exception"""

    pass


class CredentialsError(JamfProSdkException):
    """Credentials Error"""

    pass
