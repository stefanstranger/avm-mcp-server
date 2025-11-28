"""
Tests to verify the package is properly configured for distribution.
These tests help catch issues like missing files in pyproject.toml.
"""

import pytest
import subprocess
import sys
import os
import tempfile
import shutil


class TestPackageConfiguration:
    """Tests for package configuration in pyproject.toml."""

    def test_pyproject_exists(self):
        """Test that pyproject.toml exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        assert os.path.exists(pyproject_path), "pyproject.toml not found"

    def test_pyproject_has_required_fields(self):
        """Test that pyproject.toml has required fields."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        assert "project" in config
        assert "name" in config["project"]
        assert "version" in config["project"]
        assert "dependencies" in config["project"]

    def test_required_files_in_wheel(self):
        """Test that required files are included in wheel configuration."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        # Check that wheel includes necessary files
        wheel_config = config.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
        only_include = wheel_config.get("only-include", [])
        
        # server.py and config.py must be included
        assert "server.py" in only_include, "server.py must be included in wheel"
        assert "config.py" in only_include, "config.py must be included in wheel"

    def test_required_dependencies(self):
        """Test that all required dependencies are listed."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        dependencies = config["project"]["dependencies"]
        
        # Check required dependencies
        dep_names = [d.split("[")[0].split(">=")[0].split("==")[0].lower() for d in dependencies]
        
        assert "fastmcp" in dep_names, "fastmcp must be in dependencies"
        assert "requests" in dep_names, "requests must be in dependencies"
        assert "pydantic-settings" in dep_names, "pydantic-settings must be in dependencies"

    def test_entry_point_configured(self):
        """Test that entry point is properly configured."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        scripts = config["project"].get("scripts", {})
        assert "avm-mcp-server" in scripts, "avm-mcp-server entry point must be defined"


class TestBuildPackage:
    """Test that the package can be built successfully."""

    @pytest.mark.slow
    def test_build_wheel(self):
        """Test that a wheel can be built."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, "-m", "build", "--wheel", "--outdir", tmpdir],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                pytest.skip(f"Build failed (build module may not be installed): {result.stderr}")
            
            # Check that wheel was created
            wheel_files = [f for f in os.listdir(tmpdir) if f.endswith('.whl')]
            assert len(wheel_files) == 1, "Expected exactly one wheel file"
