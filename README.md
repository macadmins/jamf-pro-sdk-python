# Jamf Pro SDK for Python

A client library for the Jamf Pro APIs and webhooks.

```python
from jamf_pro_sdk import JamfProClient, BasicAuthProvider

client = JamfProClient(
    server="dummy.jamfcloud.com",
    credentials=BasicAuthProvider("username", "password")
)

all_computers = client.pro_api.get_computer_inventory_v1()
```

Read the full documentation on [GitHub Pages](https://macadmins.github.io/jamf-pro-sdk-python/).

## Installing

Install from PyPI:

```console
% python -m pip install jamf-pro-sdk
```

The Jamf Pro SDK supports Python 3.9+.
