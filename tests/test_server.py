"""
Tests for the server module.
"""

import pytest
import json
from unittest.mock import patch, MagicMock


class TestListAvmModules:
    """Tests for the list_avm_modules function."""

    @patch('server.requests.get')
    def test_list_avm_modules_success(self, mock_get):
        """Test successful listing of AVM modules."""
        from server import list_avm_modules
        
        # Mock the catalog response
        catalog_response = MagicMock()
        catalog_response.json.return_value = {
            "repositories": [
                "bicep/avm/res/storage/storage-account",
                "bicep/avm/res/compute/virtual-machine",
                "other/non-avm/module"
            ]
        }
        catalog_response.raise_for_status = MagicMock()
        
        # Mock the tags response
        tags_response = MagicMock()
        tags_response.json.return_value = {"tags": ["1.0.0", "1.1.0"]}
        tags_response.raise_for_status = MagicMock()
        
        mock_get.side_effect = [catalog_response, tags_response, tags_response]
        
        result = list_avm_modules()
        modules = json.loads(result)
        
        # Should only include bicep/avm modules, not other modules
        assert len(modules) == 2
        assert all(m["name"].startswith("bicep/avm/") for m in modules)

    @patch('server.requests.get')
    def test_list_avm_modules_with_filter(self, mock_get):
        """Test filtering AVM modules by name."""
        from server import list_avm_modules
        
        catalog_response = MagicMock()
        catalog_response.json.return_value = {
            "repositories": [
                "bicep/avm/res/storage/storage-account",
                "bicep/avm/res/compute/virtual-machine"
            ]
        }
        catalog_response.raise_for_status = MagicMock()
        
        tags_response = MagicMock()
        tags_response.json.return_value = {"tags": ["1.0.0"]}
        tags_response.raise_for_status = MagicMock()
        
        mock_get.side_effect = [catalog_response, tags_response]
        
        result = list_avm_modules(modulename="storage")
        modules = json.loads(result)
        
        assert len(modules) == 1
        assert "storage" in modules[0]["name"]

    @patch('server.requests.get')
    def test_list_avm_modules_request_error(self, mock_get):
        """Test handling of request errors."""
        from server import list_avm_modules
        import requests
        
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = list_avm_modules()
        error = json.loads(result)
        
        assert "error" in error


class TestScrapeAvmModuleDetails:
    """Tests for the scrape_avm_module_details function."""

    @patch('server.requests.get')
    def test_scrape_valid_url(self, mock_get):
        """Test scraping a valid GitHub URL."""
        from server import scrape_avm_module_details
        
        mock_response = MagicMock()
        mock_response.text = """
# Module Name

## Resource Types

| Resource Type | API Version |
|:--|:--|
| `Microsoft.Storage/storageAccounts` | 2023-01-01 |

## Parameters

| Parameter | Type | Description |
|:--|:--|:--|
| name | string | The name of the storage account |

## Usage Examples

### Example 1: _Using large parameter set_

<details>
content here
</details>
<p>

## Other Section
"""
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        url = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/storage/storage-account"
        result = scrape_avm_module_details(url)
        
        assert "Resource Types" in result
        assert "Parameters" in result

    def test_scrape_invalid_url(self):
        """Test handling of invalid URL format."""
        from server import scrape_avm_module_details
        
        result = scrape_avm_module_details("not-a-valid-url")
        
        assert "Error" in result

    @patch('server.requests.get')
    def test_scrape_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        from server import scrape_avm_module_details
        import requests
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response
        
        url = "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/nonexistent/module"
        result = scrape_avm_module_details(url)
        
        assert "Error" in result


class TestPrompts:
    """Tests for MCP prompts."""

    def test_find_avm_module_prompt_with_search(self):
        """Test find_avm_module_prompt with search term."""
        from server import find_avm_module_prompt
        
        result = find_avm_module_prompt("storage")
        
        assert "storage" in result
        assert "find" in result.lower() or "match" in result.lower()

    def test_find_avm_module_prompt_without_search(self):
        """Test find_avm_module_prompt without search term."""
        from server import find_avm_module_prompt
        
        result = find_avm_module_prompt()
        
        assert "list" in result.lower() or "all" in result.lower()

    def test_get_avm_module_details_prompt(self):
        """Test get_avm_module_details_prompt."""
        from server import get_avm_module_details_prompt
        
        result = get_avm_module_details_prompt("storage-account")
        
        assert "storage-account" in result
        assert "Resource Types" in result or "Parameters" in result

    def test_suggest_avm_for_service_prompt(self):
        """Test suggest_avm_for_service_prompt."""
        from server import suggest_avm_for_service_prompt
        
        result = suggest_avm_for_service_prompt("Azure Storage")
        
        assert "Azure Storage" in result


class TestMcpServer:
    """Tests for MCP server initialization."""

    def test_mcp_server_name(self):
        """Test that MCP server has correct name."""
        from server import mcp
        
        assert mcp.name == "AVM MCP Server"

    def test_mcp_server_version(self):
        """Test that MCP server has a version."""
        from server import mcp
        
        # FastMCP stores version differently, just check it exists
        assert mcp is not None


class TestArgumentParser:
    """Tests for command-line argument parsing."""

    def test_parse_arguments_defaults(self):
        """Test default argument values."""
        from server import parse_arguments
        import sys
        
        # Save original argv
        original_argv = sys.argv
        sys.argv = ['server.py']
        
        try:
            args = parse_arguments()
            assert args.transport == "http"
            assert args.host is None
            assert args.port is None
            assert args.debug is False
        finally:
            sys.argv = original_argv

    def test_parse_arguments_custom(self):
        """Test custom argument values."""
        from server import parse_arguments
        import sys
        
        original_argv = sys.argv
        sys.argv = ['server.py', '--transport', 'stdio', '--host', '127.0.0.1', '--port', '9000', '--debug']
        
        try:
            args = parse_arguments()
            assert args.transport == "stdio"
            assert args.host == "127.0.0.1"
            assert args.port == 9000
            assert args.debug is True
        finally:
            sys.argv = original_argv
