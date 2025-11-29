"""
Essential tests to catch packaging and import issues before release.
These tests specifically target issues that have caused runtime failures.
"""

import os


class TestPackageEssentials:
    """Essential package validation tests."""

    def get_pyproject_config(self):
        """Load pyproject.toml configuration."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            return tomllib.load(f)

    def test_required_files_in_wheel(self):
        """
        Test that required files are included in wheel.
        
        This catches the issue where config.py was missing from the wheel,
        causing: ModuleNotFoundError: No module named 'config'
        """
        config = self.get_pyproject_config()
        wheel_config = config.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
        only_include = wheel_config.get("only-include", [])
        
        assert "server.py" in only_include, "server.py must be in wheel"
        assert "config.py" in only_include, "config.py must be in wheel"

    def test_required_dependencies(self):
        """
        Test that all required dependencies are listed.
        
        This catches missing dependencies that cause import failures.
        """
        config = self.get_pyproject_config()
        dependencies = config["project"]["dependencies"]
        dep_names = [d.split("[")[0].split(">=")[0].split("==")[0].lower() for d in dependencies]
        
        assert "fastmcp" in dep_names, "fastmcp required"
        assert "requests" in dep_names, "requests required"
        assert "pydantic-settings" in dep_names, "pydantic-settings required"
        assert "nest-asyncio" in dep_names, "nest-asyncio required for HTTP/SSE"

    def test_entry_point_configured(self):
        """Test that CLI entry point is configured."""
        config = self.get_pyproject_config()
        scripts = config["project"].get("scripts", {})
        assert "avm-mcp-server" in scripts, "avm-mcp-server entry point required"


class TestImportsWork:
    """Verify all modules can be imported without errors."""

    def test_modules_import(self):
        """
        Test that all modules can be imported.
        
        This catches missing dependencies and modules not in the wheel.
        """
        import config
        import server
        
        assert config.settings is not None
        assert server.mcp is not None
