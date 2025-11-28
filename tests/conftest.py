"""
Pytest configuration and fixtures.
"""

import pytest
import sys
import os

# Add the project root to the path so we can import modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture
def mock_avm_catalog_response():
    """Fixture providing a mock AVM catalog response."""
    return {
        "repositories": [
            "bicep/avm/res/storage/storage-account",
            "bicep/avm/res/compute/virtual-machine",
            "bicep/avm/res/network/virtual-network",
            "bicep/avm/ptn/app/container-app",
            "other/non-avm/repository"
        ]
    }


@pytest.fixture
def mock_tags_response():
    """Fixture providing a mock tags response."""
    return {
        "tags": ["0.1.0", "0.2.0", "1.0.0"]
    }


@pytest.fixture
def sample_readme_content():
    """Fixture providing sample README content for scraping tests."""
    return """
# Azure Verified Module - Storage Account

## Resource Types

| Resource Type | API Version |
|:--|:--|
| `Microsoft.Storage/storageAccounts` | 2023-01-01 |
| `Microsoft.Storage/storageAccounts/blobServices` | 2023-01-01 |

## Parameters

**Required parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| name | string | The name of the storage account. |
| location | string | Location for all resources. |

**Optional parameters**

| Parameter | Type | Description |
|:--|:--|:--|
| sku | string | Storage account SKU. |
| kind | string | Storage account kind. |

## Usage Examples

### Example 1: _Using only defaults_

<details>
<summary>via Bicep module</summary>

```bicep
module storageAccount 'br:mcr.microsoft.com/bicep/avm/res/storage/storage-account:1.0.0' = {
  name: 'storageAccount'
  params: {
    name: 'mystorageaccount'
  }
}
```

</details>
<p>

### Example 2: _Using large parameter set_

<details>
<summary>via Bicep module</summary>

```bicep
module storageAccount 'br:mcr.microsoft.com/bicep/avm/res/storage/storage-account:1.0.0' = {
  name: 'storageAccount'
  params: {
    name: 'mystorageaccount'
    sku: 'Standard_LRS'
    kind: 'StorageV2'
    location: 'eastus'
    // Additional parameters
  }
}
```

</details>
<p>

## Other Section

This is other content.
"""
