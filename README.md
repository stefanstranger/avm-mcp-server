# 🏗️ avm-mcp-server

MCP Server for discovering and exploring Azure Verified Modules (AVM) from the Bicep Public Registry.

## 🎯 Overview

This MCP server enables AI agents and tools to search, discover, and retrieve detailed information about Azure Verified Modules (AVM) via the Model Context Protocol (MCP). It connects directly to the Microsoft Container Registry (MCR) and GitHub to provide up-to-date module information, versions, parameters, and usage examples.

## ❓ Why AVM MCP Server?

Azure Verified Modules (AVM) are a collection of standardized, validated, and well-documented Infrastructure as Code (IaC) modules for deploying Azure resources using Bicep. However, discovering the right module and understanding its parameters can be challenging:

- **Discovery Challenge**: With hundreds of AVM modules available, finding the right module for your use case requires searching through documentation
- **Parameter Complexity**: Each module has numerous parameters with specific requirements and defaults
- **Version Management**: Keeping track of module versions and updates across the registry
- **Documentation Access**: Module documentation is scattered across GitHub repositories

This MCP server solves these challenges by:

- Providing fast, intelligent search across all AVM modules
- Retrieving module versions directly from the registry
- Extracting detailed parameter information and usage examples
- Enabling AI agents to help you find and use the right modules

## Comparison with Microsoft Bicep MCP Server

Microsoft provides an [official Bicep MCP Server](https://github.com/Azure/bicep) that includes a `ListAvmMetadata` tool. So why create a separate AVM MCP Server?

### Key Differences

| Feature | Microsoft Bicep MCP Server | AVM MCP Server (This Project) |
|---------|---------------------------|-------------------------------|
| **Primary Focus** | Bicep language tools & Azure resource schemas | AVM module discovery & documentation |
| **AVM Module Search** | Lists all modules (no filtering) | Intelligent search with multiple query formats |
| **Module Details** | Basic metadata (name, description, versions) | Deep documentation extraction (parameters, resource types, examples) |
| **Installation** | Requires .NET runtime & Bicep CLI | Lightweight Python with minimal dependencies |
| **Response Format** | Newline-separated text summary | Structured JSON with rich metadata |
| **Documentation Access** | External links only | Extracted and formatted markdown from module READMs |

### Why This Server Exists

While the official Bicep MCP Server is excellent for **authoring Bicep templates** and accessing Azure resource type schemas, it provides limited functionality for **discovering and understanding AVM modules**:

1. **No Search Capability**: The `ListAvmMetadata` tool returns ALL modules without filtering, making it difficult to find relevant modules when there are hundreds available. This server provides intelligent search that handles variations like "key vault", "key-vault", and "keyvault".

2. **Limited Documentation**: The official tool provides only basic metadata (name, description, versions, documentation URI). This server extracts the actual documentation content including:
   - Complete parameter reference with types and descriptions
   - Resource types deployed by the module
   - Real-world usage examples with large parameter sets

3. **Different Use Cases**: 
   - **Use Bicep MCP Server when**: Writing Bicep code, checking Azure resource schemas, following Bicep best practices
   - **Use AVM MCP Server when**: Discovering which AVM module to use, understanding module parameters, exploring module capabilities

4. **Complementary Tools**: These servers can work together! Use the Bicep MCP Server for template authoring and this server for module discovery and documentation.

### When to Use Each

**Choose Microsoft Bicep MCP Server if you need:**

- Bicep authoring best practices
- Azure resource type schemas and API versions
- Comprehensive Bicep ecosystem tools

**Choose AVM MCP Server if you need:**

- Find AVM modules for specific Azure services
- Understand module parameters before using them
- Extract usage examples and documentation
- Quick filtered search across the AVM catalog

**Use both servers together for a complete Bicep + AVM development experience!**

## 🛠️ Features

- **Search AVM Modules**: Intelligent search supporting multiple query formats (e.g., "key vault", "key-vault", "keyvault")
- **List Module Versions**: Retrieve all available versions for any AVM module
- **Module Details**: Extract resource types, parameters, and usage examples from module documentation
- **Fast Filtering**: Optimized search that quickly narrows down results from thousands of repositories
- **Direct Registry Access**: Connects to Microsoft Container Registry for real-time module information

## 📋 Prerequisites

- Python 3.11 or higher
- UV package manager
- Internet connectivity (to access Microsoft Container Registry and GitHub)
- Node.js and npm (for MCP inspector tools, optional)

### 1. Python

- **Official Download Page:**  
  [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Direct Download for Python 3.11.14:**  
  [Python 3.11.14 Release Page](https://www.python.org/downloads/release/python-31114/)

- Download the installer for your OS (Windows, macOS, Linux) and follow the setup instructions.

---

### 2. UV (Python Package Manager)

- **Official Documentation & Source:**  
  [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)  
  [UV Documentation](https://docs.astral.sh/uv/)

- **Installation (Windows):**

  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

    Or, using pip (if you already have Python and pip installed):

  ```powershell
  pip install uv
  ```

- **Installation (macOS/Linux):**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **More Info:**  
  [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Claude Desktop (Optional)

- **Official Download Page:**  
  [https://claude.ai/download](https://claude.ai/download)

- Download the installer for your OS (Windows, macOS) and follow the setup instructions.

## 🚀 Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/stefanstranger/avm-mcp-server.git
   cd avm-mcp-server
   ```

2. Create a virtual environment:

   ```powershell
   uv venv .venv --python 3.13
   ```

3. Activate the virtual environment:
   - **Windows PowerShell:**
  
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

   - **macOS/Linux:**

     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:

   ```powershell
   uv pip install fastmcp requests
   ```

## ⚙️ Configuration

### 🔧 Claude Desktop Setup

#### Option 1: Using uvx with GitHub Repository (Recommended)

Use the following command to add the AVM MCP server to your local environment. This assumes uvx is in your $PATH; if not, then you need to provide the full path to uvx.

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "avm-mcp-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/stefanstranger/avm-mcp-server",
        "avm-mcp-server"
      ]
    }
  }
}
```

This approach:

- ✅ No local installation required
- ✅ Always uses the latest version from the main branch
- ✅ No need to manage virtual environments
- ✅ Works across different machines with the same config

To use a specific version/tag, modify the GitHub URL:

```json
"git+https://github.com/stefanstranger/avm-mcp-server@v0.1.3"
```

#### Option 2: Using Local Installation

If you prefer to run from a local clone:

```json
{
  "mcpServers": {
    "avm-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "requests",
        "mcp",
        "run",
        "C:\\Github\\avm-mcp-server\\server.py"
      ]
    }
  }
}
```

**Note**: Adjust the path in the last `args` element to match your installation location.

## 🏃 Running the Server

### Using uvx (No Installation Required)

Run directly from GitHub:

```powershell
uvx --from git+https://github.com/stefanstranger/avm-mcp-server avm-mcp-server
```

Or with a specific version:

```powershell
uvx --from git+https://github.com/stefanstranger/avm-mcp-server@v0.1.0 avm-mcp-server
```

### Using Local Installation

If you cloned the repository:

```powershell
uv run .\server.py
```

### Inspect MCP Server

Using the MCP Inspector with uvx:

```powershell
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/stefanstranger/avm-mcp-server avm-mcp-server
```

Using the MCP Inspector with local installation:

```powershell
npx @modelcontextprotocol/inspector uv run --with mcp[cli] mcp run c://github//avm-mcp-server//server.py
```

Using mcptools:

```powershell
mcptools web cmd /c "uvx.exe --from git+https://github.com/stefanstranger/avm-mcp-server avm-mcp-server"
```

## 📖 Available Tools

### 1. `list_avm_modules`

Search and list Azure Verified Modules from the Bicep Public Registry.

**Parameters:**

- `modulename` (optional): Module name to filter by. Supports multiple formats:
  - Exact match: `"storage-account"`
  - Hyphenated: `"key-vault"`
  - Space-separated: `"key vault"` (matches "key-vault", "keyvault", "key", or "vault")
  - Compact: `"keyvault"`

**Returns:**
JSON array with module information including:

- Module name (registry path)
- Available versions
- Description
- Documentation link

**Example Usage:**

```text
"List all AVM modules for storage accounts"
"Find Azure Verified Modules for key vault"
"Show me AVM modules related to networking"
```

**Example Response:**

```json
[
  {
    "name": "bicep/avm/res/storage/storage-account",
    "versions": ["0.9.1", "0.9.0", "0.8.3"],
    "description": "Azure Verified Module",
    "documentation": "https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/storage/storage-account"
  }
]
```

### 2. `scrape_avm_module_details`

Fetch detailed information from an AVM module's README documentation.

**Parameters:**

- `url` (required): GitHub URL of the AVM module repository
  - Example: `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/storage/storage-account`

**Returns:**
Formatted markdown containing:

- **Resource Types**: Azure resources deployed by the module
- **Parameters**: Complete parameter reference with types, defaults, and descriptions
- **Usage Examples**: Large parameter set examples showing real-world usage

**Example Usage:**

```text
"Get the details for the storage account AVM module"
"Show me the parameters for the key vault module"
"What resources does the virtual network module deploy?"
```

**Example Response:**

```markdown
## Resource Types

| Resource Type | API Version |
| :-- | :-- |
| `Microsoft.Storage/storageAccounts` | [2022-09-01] |
| `Microsoft.Storage/storageAccounts/blobServices` | [2022-09-01] |

## Parameters

**Required parameters**

| Parameter | Type | Description |
| :-- | :-- | :-- |
| [`name`](#parameter-name) | string | Name of the Storage Account. |

**Optional parameters**

| Parameter | Type | Description |
| :-- | :-- | :-- |
| [`location`](#parameter-location) | string | Location for all resources. |
...
```

## 📖 Available Prompts

### 1. `find_avm_module_prompt`

A prompt to find Azure Verified Modules (AVM).

**Parameters:**

- `search_term` (optional): The search term to use to find AVM modules.

**Example Usage:**

```text
"Find AVM modules for 'storage account'"
```

### 2. `get_avm_module_details_prompt`

A prompt to get the details of a specific AVM.

**Parameters:**

- `module_name` (required): The name of the AVM module.

**Example Usage:**

```text
"Get details for the 'storage-account' AVM module"
```

### 3. `suggest_avm_for_service_prompt`

A prompt to suggest an AVM for a specific Azure service.

**Parameters:**

- `azure_service` (required): The Azure service to find an AVM for.

**Example Usage:**

```text
"Suggest an AVM for 'Azure Key Vault'"
```

## 💡 Usage Examples

### Search for modules

```text
"Find all AVM modules for storage"
"List Azure Verified Modules for Key Vault"
"Show me networking modules"
```

### Get module versions

```text
"What versions are available for the storage account module?"
"List all versions of the AVM key vault module"
```

### Explore module details

```text
"Show me the parameters for bicep/avm/res/storage/storage-account"
"What resources does the virtual network module deploy?"
"Get usage examples for the key vault module"
```

### Combined workflows

```text
"Find the storage account AVM module and show me its parameters"
"I need to deploy a key vault - find the module and explain its parameters"
"Search for virtual network modules and show me usage examples"
```

## 🔍 How It Works

### Module Discovery

1. Queries Microsoft Container Registry's catalog endpoint (`mcr.microsoft.com/v2/_catalog`)
2. Filters repositories starting with `bicep/avm/`
3. Applies intelligent search matching:
   - Normalizes search terms (lowercase, hyphenated, compact)
   - Matches any token from multi-word queries
   - Returns all matching modules

### Version Retrieval

1. For each matching module, queries the registry's tags endpoint
2. Retrieves all available semantic versions
3. Returns version information with module metadata

### Documentation Extraction

1. Converts GitHub tree URLs to raw content URLs
2. Fetches README.md content from the bicep-registry-modules repository
3. Extracts relevant sections using regex patterns:
   - Resource Types tables
   - Parameters documentation
   - Usage examples with large parameter sets

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to fetch modules" error**
   - Check internet connectivity
   - Verify access to `mcr.microsoft.com`
   - Check for firewall/proxy restrictions

2. **"Could not fetch README.md" error**
   - Verify the GitHub URL format is correct
   - Ensure the module documentation exists in the repository
   - Check internet connectivity to `raw.githubusercontent.com`

3. **No modules found for search query**
   - Try different search terms (e.g., "storage" instead of "storage-account")
   - Use partial names (e.g., "key" to find "key-vault")
   - List all modules without a filter first

4. **Server won't start in Claude Desktop**
   - Verify Python 3.11+ is installed
   - Check that UV is properly installed
   - Ensure the path in `claude_desktop_config.json` is correct
   - Review Claude Desktop logs for detailed error messages

## Publishing & Distribution

This server is published to both PyPI and the MCP Registry for easy installation and discovery.

### Installing from PyPI

The recommended way to use this server is via `uvx` from PyPI:

```powershell
# Run directly without installation
uvx avm-mcp-server

# Or install globally
uv tool install avm-mcp-server
```

### MCP Registry

This server is registered in the [MCP Registry](https://registry.modelcontextprotocol.io/), making it discoverable by MCP clients and AI assistants.

**Registry Entry**: `io.github.stefanstranger/avm-mcp-server`

### For Developers: Publishing Updates

The project uses automated GitHub Actions workflows to publish new versions:

1. **Update Version Numbers**:
   - `pyproject.toml` - Package version
   - `server.json` - MCP registry version
   - `server.py` - FastMCP instance version

2. **Commit and Tag**:

   ```powershell
   git add pyproject.toml server.json server.py
   git commit -m "Bump version to X.Y.Z"
   git push
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

3. **Automated Workflow**:
   - GitHub Actions builds the package
   - Publishes to PyPI (requires `PYPI_API_TOKEN` secret)
   - Authenticates with MCP Registry via GitHub OIDC
   - Publishes to MCP Registry

### Manual Publishing (First Time)

For the initial PyPI release, publish manually:

```powershell
# Build the package
uv build

# Publish to PyPI (will prompt for token)
uv publish
```

**Requirements**:

- PyPI account and API token
- The README includes the MCP validation line: `<!-- mcp-name: io.github.stefanstranger/avm-mcp-server -->`

**Note**: PyPI versions cannot be re-uploaded. Always bump the version number for new releases.

## 📚 References

- [Azure Verified Modules (AVM)](https://aka.ms/AVM)
- [Bicep Registry Modules](https://github.com/Azure/bicep-registry-modules)
- [Microsoft Container Registry](https://mcr.microsoft.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Tools](https://github.com/mcptools/mcptools)

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚖️ Disclaimer

This tool is not officially affiliated with or endorsed by Microsoft or the Azure Verified Modules team. It provides read-only access to publicly available module information from the Microsoft Container Registry and GitHub.

<!-- mcp-name: io.github.stefanstranger/avm-mcp-server -->