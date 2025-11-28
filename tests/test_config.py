"""
Tests for the configuration module.
"""

import pytest
import os


class TestSettings:
    """Test Settings class configuration."""

    def test_default_host(self):
        """Test default MCP_HOST value."""
        from config import Settings
        settings = Settings()
        assert settings.MCP_HOST == "0.0.0.0"

    def test_default_port(self):
        """Test default MCP_PORT value."""
        from config import Settings
        settings = Settings()
        assert settings.MCP_PORT == 8080

    def test_default_debug(self):
        """Test default MCP_DEBUG value."""
        from config import Settings
        settings = Settings()
        assert settings.MCP_DEBUG is False

    def test_default_log_level(self):
        """Test default LOG_LEVEL value."""
        from config import Settings
        settings = Settings()
        assert settings.LOG_LEVEL == "INFO"

    def test_env_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("MCP_HOST", "127.0.0.1")
        monkeypatch.setenv("MCP_PORT", "9090")
        monkeypatch.setenv("MCP_DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        
        from config import Settings
        settings = Settings()
        
        assert settings.MCP_HOST == "127.0.0.1"
        assert settings.MCP_PORT == 9090
        assert settings.MCP_DEBUG is True
        assert settings.LOG_LEVEL == "DEBUG"


class TestLoggingConfig:
    """Test logging configuration."""

    def test_logging_config_version(self):
        """Test logging config version."""
        from config import logging_config
        assert logging_config["version"] == 1

    def test_logging_config_has_console_handler(self):
        """Test that console handler is configured."""
        from config import logging_config
        assert "console" in logging_config["handlers"]

    def test_logging_config_formatter(self):
        """Test that default formatter is configured."""
        from config import logging_config
        assert "default" in logging_config["formatters"]
        assert "format" in logging_config["formatters"]["default"]
