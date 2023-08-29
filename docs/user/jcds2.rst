JCDS2
=====

The JCDS2 client provides interfaces for uploading and downloading files to the Jamf Cloud Distribution Service v2 (JCDS2, or just referred to as JCDS).

Installation Requirements
-------------------------

For file uploads the JCDS2 client requires additional dependencies not included with the default installation of the SDK.

.. code-block:: console

    (.venv) % pip install 'jamf-pro-sdk[aws]'

File downloads do not require any additional dependencies and can be used with the base install.

About Packages, Files, and Distribution Points
----------------------------------------------

There are two separate objects across the Classic and Pro APIs for managing packages that can be deployed.

* **Package** objects are only available through the Classic API.
* **File** objects are only available through the Pro API and specifically are only relevant to the JCDS.

Packages and files are associated to each other in Jamf Pro, but it is not required. Consider these cases:

* In order for a file to be included with a policy it **must** have a package object.
* Installing a package using an MDM command **does not** require a package object.

.. caution::

    It is important to note that a Jamf Pro package can be created using the API and provided the associated filename without performing any upload through the GUI or APIs, and a JCDS file can be uploaded without being associated with a Jamf Pro package.

    Conversely, deleting a package object that is associated to a JCDS file will delete the file, but deleting a JCDS file associated to a package does not delete the package.

.. tip::

    If you only use the JCDS for package distribution in your environment you may skip the rest of this section.

In environments where multiple types of distribution points exists your file management may vary. The JCDS is often the default, and only, distribution point for **Jamf Cloud** customers.

Local file distribution points (such as servers/hosts serving traffic over an office network) are managed independently of Jamf Pro.

Cloud Distribution points (Akami, AWS, and Rackspace) support file uploads from the Jamf Pro web GUI when creating packages, but not through any supported API.

The JCDS2 client can only manage files that in the JCDS. If you use other types of file distribution points in your environment you will need to handle the upload operations but can use the SDK to create the package objects with :meth:`~jamf_pro_sdk.clients.classic_api.ClassicApi.create_package`.

Uploading Files
---------------

The file upload operation performs multiple API requests in sequence.

* All packages in Jamf Pro will be read and checked to see if the filename is already in use by a package (whether or not the file is in the JCDS or doesn't exist in any distribution point).
* A new JCDS file will be created returning temporary IAM credentials to the client.
* If the file is less than 1 GiB in size the upload will be performed in a single request.
* If the file is greater than 1 GiB in size a multipart upload operation will be performed.
* The package object will be created for the file upon success.

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider
    >>> client = JamfProClient("dummy.jamfcloud.com", BasicAuthProvider("demo", "tryitout"))
    >>> client.jcds2.upload_file(file_path="/path/to/my.pkg")
    >>>

Downloading Files
-----------------

File downloads will retrieve the download URL to the requested JCDS file and then save it to the path provided. If the path is a directory the filename is appended automatically.

.. code-block:: python

    >>> from jamf_pro_sdk import JamfProClient, BasicAuthProvider
    >>> client = JamfProClient("dummy.jamfcloud.com", BasicAuthProvider("demo", "tryitout"))
    >>> client.jcds2.download_file(file_name="/path/to/my.pkg", download_path="/path/to/downloads/")
    >>>

Download operations retrieve the file in 20 MiB chunks using range requests. The SDK is able to handle extremely large file sizes in this way.
