# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-11-29

### Added

- Distribution tests (`tests/test_distribution.py`) to catch packaging issues before release
- CI workflow (`test.yml`) to run tests on push and pull requests
- Tests now run before publishing to PyPI/MCP Registry
- CHANGELOG.md to document changes
- Automated git tagging on merge to main (no manual tagging required)
- VS Code tasks for version checking and running tests (`.vscode/tasks.json`)
- Version check script (`scripts/check_version.py`) to validate version bump before release
- Docker documentation in README
- Setup script documentation for Linux/macOS users

### Changed

- Publish workflow now triggers on merge to main instead of manual tags
- Version is automatically detected from `pyproject.toml`
- Git tags are created automatically by the CI workflow
- Simplified test suite to 4 essential tests focused on distribution validation

### Fixed

- Fixed missing `config.py` in wheel package distribution
- Added missing `pydantic-settings` dependency to `pyproject.toml`
- Fixed MCP STDIO transport JSON parse errors by redirecting logging to stderr
- Added missing `nest-asyncio` dependency required for HTTP/SSE transports

## [0.1.4] - 2025-11-27

### Initial Release

- `list_avm_modules` tool to list and search Azure Verified Modules
- `scrape_avm_module_details` tool to extract module documentation
- Support for multiple transport methods: HTTP, SSE, and STDIO
- Configuration via environment variables
- Docker support
- MCP prompts for finding and suggesting AVM modules
- Search AVM modules by name
- Get module versions and documentation links
- Extract Resource Types, Parameters, and Usage Examples from module READMEs
- Configurable host, port, and debug settings

[0.1.5]: https://github.com/stefanstranger/avm-mcp-server/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/stefanstranger/avm-mcp-server/releases/tag/v0.1.4
