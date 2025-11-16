import requests
import json
import re
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AVM MCP Server", "0.1.3")


@mcp.tool()
def list_avm_modules(modulename: Optional[str] = None) -> str:
    """
    List Azure Verified Modules (AVM).
    If modulename is provided, return details for that specific module.

    Args:
        modulename (str): AVM Module name to filter by

    Returns:
        str: a list of AVM modules in JSON format with their versions and documentation links
    """
    try:
        # Get the list of AVM modules in JSON format
        response = requests.get("https://mcr.microsoft.com/v2/_catalog?n=10000")
        response.raise_for_status()
        repositories = response.json().get("repositories", [])
        search_terms = None
        if modulename:
            normalized = modulename.lower()
            compact = normalized.replace(" ", "")
            hyphenated = normalized.replace(" ", "-")
            tokens = normalized.split()
            search_terms = {
                normalized,
                compact,
                hyphenated,
                *tokens,
            }

        avm_modules = []
        for repo in repositories:
            if not repo.startswith("bicep/avm/"):
                continue

            repo_lower = repo.lower()
            if search_terms and not any(term in repo_lower for term in search_terms):
                continue

            print(f"Processing: {repo}")
            tags_response = requests.get(f"https://mcr.microsoft.com/v2/{repo}/tags/list")
            tags_response.raise_for_status()
            tags_data = tags_response.json()

            module_info = {
                "name": repo,
                "versions": tags_data.get("tags", []),
                "description": "Azure Verified Module",
                "documentation": f"https://github.com/Azure/bicep-registry-modules/tree/main{repo.replace('bicep', '')}"
            }
            avm_modules.append(module_info)

        return json.dumps(avm_modules, indent=2)

    except requests.RequestException as e:
        return json.dumps({"error": f"Failed to fetch modules: {str(e)}"}, indent=2)


@mcp.tool()
def scrape_avm_module_details(url: Optional[str] = None) -> str:
    """
    Fetch and extract specific sections from AVM module README.md, returning formatted markdown.

    Extracts:
    - Resource Types
    - Parameters
    - Usage Examples (focusing on large parameter sets)

    Converts GitHub URLs like:
    https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/storage/storage-account

    To raw URLs like:
    https://raw.githubusercontent.com/Azure/bicep-registry-modules/refs/heads/main/avm/res/storage/storage-account/README.md

    Args:
        url (str): AVM GitHub repository URL

    Returns:
        str: Formatted markdown string containing the extracted sections
    """
    try:
        # Parse GitHub URL to extract owner, repo, branch, and path
        github_pattern = r'https://github\.com/([^/]+)/([^/]+)/(tree|blob)/([^/]+)/(.+)'
        match = re.match(github_pattern, url)

        owner, repo, view_type, branch, path = match.groups()

        # Construct raw GitHub URL for README.md using refs/heads/ format
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{path}/README.md"

        print(f"Fetching: {raw_url}")

        # Fetch the raw markdown content
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()

        content = response.text

        # Build markdown output
        markdown_output = []

        # Extract Resource Types section
        resource_types_match = re.search(
            r'(## Resource Types.*?)(##\s+)',
            content,
            re.DOTALL | re.MULTILINE
        )
        if resource_types_match:
            markdown_output.append(resource_types_match.group(1).strip())
            markdown_output.append("\n")

        # Extract Parameters section
        parameters_match = re.search(
            r'(## Parameters.*?)(##\s+)',
            content,
            re.DOTALL | re.MULTILINE
        )
        if parameters_match:
            markdown_output.append(parameters_match.group(1).strip())
            markdown_output.append("\n")

        # Extract the "Using large parameter set" example directly from the full content
        # This pattern matches from "### Example X: _Using large parameter set_"
        # to the last "</details>\n<p>" which marks the end of that example
        large_param_match = re.search(
            r'(###\s+Example\s+\d+:\s+_Using\s+large\s+parameter\s+set_.*?</details>\s*<p>)',
            content,
            re.DOTALL
        )
        if large_param_match:
            markdown_output.append(large_param_match.group(1).strip())

        return "\n".join(markdown_output)

    except requests.exceptions.HTTPError as e:
        return f"# Error\n\nCould not fetch README.md from {url}. Status code: {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"# Error\n\nError fetching {url}: {str(e)}"
    except Exception as e:
        return f"# Error\n\nError processing {url}: {str(e)}"


@mcp.prompt()
def find_avm_module_prompt(search_term: str | None = None) -> str:
    """
    A prompt to find Azure Verified Modules (AVM).
    """
    if search_term:
        return f"""
        Please find the AVM modules that match the search term '{search_term}'.
        For each module, provide the name, versions, and a link to the documentation.
        """
    else:
        return f"""
        Please list all available Azure Verified Modules (AVM).
        For each module, provide the name, versions, and a link to the documentation.
        """


@mcp.prompt()
def get_avm_module_details_prompt(module_name: str) -> str:
    """
    A prompt to get the details of a specific AVM.
    """
    return f"""
    Please provide the details for the AVM module '{module_name}'.
    I am interested in the Resource Types, Parameters, and Usage Examples.
    Make sure you include the latest version available in the Usage Examples.
    """


@mcp.prompt()
def suggest_avm_for_service_prompt(azure_service: str) -> str:
    """
A prompt to suggest an AVM for a specific Azure service.
    """
    return f"""
    I need to deploy a '{azure_service}' in Azure.
    Can you suggest a suitable Azure Verified Module (AVM) for this?
    Please provide the module name and why you are suggesting it.
    """
