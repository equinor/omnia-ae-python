# omnia-ae-python
Official Python SDK for the Omnia Alarm &amp; Events API

Python package for interacting with the [Omnia Industrial IoT Alarm & Events API](https://github.com/equinor/OmniaPlant/wiki).

## How do I get set up? ###

To use the Python package, install it in the following manner:

```
$ pip install git+https://github.com/equinor/omnia-ae-python.git@main
```

For support, create an issue on GitHub.

### Development

To start developing the package, install it in editable mode:

```
$ git clone https://github.com/equinor/omnia-ae-python
$ cd omnia-ae-python
$ pip install -e .
```

## Example usage

### Preparing Azure authentication

See https://github.com/equinor/OmniaPlant/wiki/Authentication-&-Authorization for general information about Alarm & Events API authentication and authorization.

#### With service principal credentials

```python
from azure.identity import ClientSecretCredential
import os
credential = ClientSecretCredential(
    tenant_id=os.environ['AZURE_TENANT_ID'],
    client_id=os.environ['AZURE_CLIENT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET']
)
```

#### With user impersonation

For testing user impersonation you can use our public client ids:

- 67da184b-6bde-43fd-a155-30ed4ff162d2 (test)
- 141369bd-3dca-4b55-825b-56ad4a69b1fc (production)

```python
from azure.identity import DeviceCodeCredential
import os
credential = DeviceCodeCredential(
    tenant_id=os.environ['AZURE_TENANT_ID'],
    client_id=os.environ['AZURE_CLIENT_ID']
)
```

During authentication, this will display a URL to visit, and a code to enter. After completing
the flow, execution will proceed.

TODO : Need to add more here
