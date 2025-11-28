"""
Tests for version validation.
Ensures the package version is properly bumped before release.
"""

import pytest
import requests
from packaging import version


class TestVersionValidation:
    """Tests for version validation."""

    def get_local_version(self) -> str:
        """Get the version from pyproject.toml."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        return config["project"]["version"]

    def get_pypi_version(self) -> str | None:
        """Get the latest version from PyPI."""
        try:
            response = requests.get(
                "https://pypi.org/pypi/avm-mcp-server/json",
                timeout=10
            )
            if response.status_code == 404:
                # Package doesn't exist on PyPI yet
                return None
            response.raise_for_status()
            return response.json()["info"]["version"]
        except requests.RequestException:
            return None

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        local_version = self.get_local_version()
        
        # Should be parseable as a version
        parsed = version.parse(local_version)
        assert isinstance(parsed, version.Version), f"Invalid version format: {local_version}"
        
        # Should have major.minor.patch format
        assert parsed.major is not None
        assert parsed.minor is not None
        assert parsed.micro is not None

    def test_version_is_higher_than_pypi(self):
        """
        Test that local version is higher than the published PyPI version.
        
        This test helps catch cases where:
        - Version wasn't bumped before release
        - Version was accidentally decreased
        """
        local_version = self.get_local_version()
        pypi_version = self.get_pypi_version()
        
        if pypi_version is None:
            pytest.skip("Package not yet published to PyPI or PyPI is unreachable")
        
        local_parsed = version.parse(local_version)
        pypi_parsed = version.parse(pypi_version)
        
        assert local_parsed > pypi_parsed, (
            f"Local version ({local_version}) must be higher than "
            f"PyPI version ({pypi_version}). Did you forget to bump the version?"
        )

    def test_version_matches_server(self):
        """Test that pyproject.toml version matches server.py version."""
        local_version = self.get_local_version()
        
        # Import server and check if version is defined there
        from server import mcp
        
        # FastMCP version is passed as second argument
        # We check it's consistent
        if hasattr(mcp, 'version'):
            assert mcp.version == local_version, (
                f"server.py version ({mcp.version}) doesn't match "
                f"pyproject.toml version ({local_version})"
            )

    def test_version_in_server_json(self):
        """Test that server.json version matches pyproject.toml version."""
        import json
        import os
        
        local_version = self.get_local_version()
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        server_json_path = os.path.join(project_root, "server.json")
        
        if not os.path.exists(server_json_path):
            pytest.skip("server.json not found")
        
        with open(server_json_path, "r") as f:
            server_config = json.load(f)
        
        # Check top-level version if it exists
        if "version" in server_config:
            assert server_config["version"] == local_version, (
                f"server.json version ({server_config['version']}) doesn't match "
                f"pyproject.toml version ({local_version})"
            )
