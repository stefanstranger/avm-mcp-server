"""Check if local version is higher than PyPI version."""
import sys

try:
    import requests
    from packaging import version
except ImportError:
    print("❌ Missing dependencies. Run: uv sync --dev")
    sys.exit(1)


def get_local_version() -> str:
    """Get version from pyproject.toml."""
    with open("pyproject.toml", "r") as f:
        for line in f:
            if line.startswith("version = "):
                return line.split('"')[1]
    raise ValueError("Version not found in pyproject.toml")


def get_pypi_version() -> str | None:
    """Get latest version from PyPI."""
    try:
        response = requests.get(
            "https://pypi.org/pypi/avm-mcp-server/json",
            timeout=10
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.RequestException as e:
        print(f"⚠️  Could not reach PyPI: {e}")
        return None


def main():
    local = get_local_version()
    pypi = get_pypi_version()
    
    print(f"📦 Local version:  {local}")
    print(f"🌐 PyPI version:   {pypi or 'not published'}")
    print()
    
    if pypi is None:
        print("✅ Package not yet on PyPI - any version is valid")
        return 0
    
    if version.parse(local) > version.parse(pypi):
        print("✅ Version is bumped and ready for release!")
        return 0
    elif version.parse(local) == version.parse(pypi):
        print("❌ Version matches PyPI - bump the version before releasing!")
        return 1
    else:
        print("❌ Version is LOWER than PyPI - this should not happen!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
