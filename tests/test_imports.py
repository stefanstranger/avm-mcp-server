"""
Test module imports to ensure all dependencies are properly configured.
This catches issues like missing modules in pyproject.toml.
"""

import pytest


class TestModuleImports:
    """Test that all required modules can be imported."""

    def test_config_import(self):
        """Test that config module can be imported."""
        from config import settings, logging_config
        assert settings is not None
        assert logging_config is not None

    def test_config_settings_attributes(self):
        """Test that settings has expected attributes."""
        from config import settings
        assert hasattr(settings, 'MCP_HOST')
        assert hasattr(settings, 'MCP_PORT')
        assert hasattr(settings, 'MCP_DEBUG')
        assert hasattr(settings, 'LOG_LEVEL')

    def test_logging_config_structure(self):
        """Test that logging_config has the expected structure."""
        from config import logging_config
        assert 'version' in logging_config
        assert 'handlers' in logging_config
        assert 'formatters' in logging_config

    def test_server_import(self):
        """Test that server module can be imported."""
        import server
        assert hasattr(server, 'mcp')
        assert hasattr(server, 'list_avm_modules')
        assert hasattr(server, 'scrape_avm_module_details')

    def test_mcp_tools_registered(self):
        """Test that MCP tools are properly registered."""
        from server import mcp
        assert mcp is not None
        assert mcp.name == "AVM MCP Server"

    def test_third_party_imports(self):
        """Test that all third-party dependencies can be imported."""
        import requests
        import mcp
        from mcp.server.fastmcp import FastMCP
        from pydantic_settings import BaseSettings
        assert requests is not None
        assert FastMCP is not None
        assert BaseSettings is not None
