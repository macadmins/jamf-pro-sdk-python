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

Install releases from PyPI:

```console
% python -m pip install jamf-pro-sdk
```

You may also install directly from GitHub if you are testing in-development features and/or changes:

```console
% pip install git+https://github.com/macadmins/jamf-pro-sdk-python.git@<target-ref-or-branch>
```

The Jamf Pro SDK supports Python 3.9+.

# Bugs, Feedback, and Feature Requests

The Jamf Pro SDK for Python is currently in alpha. Not all APIs are available as methods through the clients, and some functionality may change during the alpha based on community feedback.

If you encounter a bug, or undesired behavior, please open a [Bug report issue](https://github.com/macadmins/jamf-pro-sdk-python/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBug%5D+Issue+title).

If you want to request or propose a change to behavior in the SDK during the alpha please oen a [Feedback issue](https://github.com/macadmins/jamf-pro-sdk-python/issues/new?assignees=&labels=feedback&projects=&template=feedback.md&title=%5BFeedback%5D+Issue+title). Feedback issues are in-between a bug report and a feature request. You are describing a current implementation (or lack thereof) and the desired change. Feedback issues are used for vetting contributions with project maintainers and the community before work begins.

If there is a feature or API you would like added (or prioritized) to the SDK please open a [Feature request issue](https://github.com/macadmins/jamf-pro-sdk-python/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature+Request%5D+Issue+title). With feature requests include a detailed description and a code example that shows how you envision the feature being used.

> For all issue templates be sure to fill out every section!

# Contributing

There are many ways to directly contribute to the project. You can enhance the documentation and user guides, or add additional API models and methods. For both there are guidelines for how to proceed.

Visit the [Contributors](https://macadmins.github.io/jamf-pro-sdk-python/contributors/index.html) section of the documentation for more details.
