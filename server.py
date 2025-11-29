import logging
import logging.config
import uvicorn
import requests
import json
import re
import argparse
import asyncio
from typing import Optional
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse, Response
from starlette.endpoints import HTTPEndpoint

# Import configuration
from config import settings, logging_config

# Configure logging
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

# Configure debug mode based on settings
if settings.MCP_DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.debug("DEBUG mode activated")

def log(message: str, level: str = "info"):
    """Helper function for consistent logging."""
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)

mcp = FastMCP("AVM MCP Server", "0.1.5")


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

            log(f"Processing: {repo}")
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

        log(f"Fetching: {raw_url}")

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


# Endpoint to list available tools in the MCP
class ToolsEndpoint(HTTPEndpoint):
    """
    Endpoint to list available tools in the MCP.
    
    This endpoint returns information about all registered tools
    in the MCP, including their names, descriptions, and expected parameters.
    """
    async def get(self, request):
        tools_list = await mcp.list_tools()
        # Convert Tool objects to dictionaries for JSON serialization
        tools_dict = {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema.model_dump() if hasattr(tool.inputSchema, 'model_dump') else tool.inputSchema
                }
                for tool in tools_list
            ]
        }
        return JSONResponse(tools_dict)


async def run_stdio() -> None:
    """
    Run the MCP server with STDIO transport.
    """
    # Suppress logging in STDIO mode to avoid interfering with JSON-RPC communication
    # Even though we log to stderr, some MCP clients may be sensitive to extra output
    logging.getLogger().setLevel(logging.WARNING)
    
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream, 
            write_stream, 
            mcp._mcp_server.create_initialization_options()
        )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the AVM MCP server with different transport methods."
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["sse", "stdio", "http"],
        default="http",
        help="Transport method to use: 'sse' (Server-Sent Events), 'stdio' (Standard I/O), or 'http' (Streamable HTTP). Default: stdio",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help=f"Host address to bind to (default: {settings.MCP_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help=f"Port to use for SSE/HTTP transport (default: {settings.MCP_PORT}). Ignored for stdio transport.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    # Override settings with command-line arguments if provided
    if args.debug:
        settings.MCP_DEBUG = True
        logger.setLevel(logging.DEBUG)
    
    log(f"Debug mode: {'ON' if settings.MCP_DEBUG else 'OFF'}")
    log(f"Transport: {args.transport.upper()}")
    
    # For stdio transport, use asyncio.run
    if args.transport == "stdio":
        asyncio.run(run_stdio(), debug=settings.MCP_DEBUG)
    else:
        # For HTTP and SSE transports, we need to handle the event loop differently
        # because uvicorn.run() creates its own event loop
        import nest_asyncio
        nest_asyncio.apply()
        
        # Use settings defaults if not provided
        host = args.host or settings.MCP_HOST
        port = args.port or settings.MCP_PORT
        
        if args.transport == "http":
            # Streamable HTTP transport
            log(f"Starting MCP server with Streamable HTTP transport at http://{host}:{port}")
            log(f"MCP Endpoint: http://{host}:{port}/mcp/")
            log(f"Tools Endpoint: http://{host}:{port}/tools")
            
            from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
            import contextlib
            from starlette.types import Receive, Scope, Send
            from typing import AsyncIterator
            
            session_manager = StreamableHTTPSessionManager(
                app=mcp._mcp_server,
                event_store=None,
                json_response=True,
                stateless=True,  # Changed to False to maintain session state
            )
            
            async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
                await session_manager.handle_request(scope, receive, send)
            
            @contextlib.asynccontextmanager
            async def lifespan(app: Starlette) -> AsyncIterator[None]:
                """Context manager for session manager."""
                async with session_manager.run():
                    try:
                        yield
                    finally:
                        log("Application shutting down...")
            
            starlette_app = Starlette(
                debug=settings.MCP_DEBUG,
                routes=[
                    Mount("/mcp/", app=handle_streamable_http),  # Added trailing slash
                    Route("/tools", ToolsEndpoint),
                ],
                lifespan=lifespan,
            )
            
            uvicorn.run(
                starlette_app, 
                host=host, 
                port=port,
                log_level="debug" if settings.MCP_DEBUG else settings.LOG_LEVEL.lower()
            )
        
        elif args.transport == "sse":
            # SSE transport
            log(f"Starting MCP server with SSE transport at http://{host}:{port}")
            log(f"SSE Endpoint: http://{host}:{port}/sse")
            log(f"Messages Endpoint: http://{host}:{port}/messages/")
            log(f"Tools Endpoint: http://{host}:{port}/tools")
            
            from mcp.server.sse import SseServerTransport
            
            sse = SseServerTransport("/messages/")
            
            async def handle_sse(request):
                async with sse.connect_sse(
                    request.scope, 
                    request.receive, 
                    request._send
                ) as (read_stream, write_stream):
                    await mcp._mcp_server.run(
                        read_stream, 
                        write_stream, 
                        mcp._mcp_server.create_initialization_options()
                    )
                return Response(status_code=204)
            
            starlette_app = Starlette(
                debug=settings.MCP_DEBUG,
                routes=[
                    Route("/sse", endpoint=handle_sse),
                    Mount("/messages/", app=sse.handle_post_message),
                    Route("/tools", ToolsEndpoint),
                ],
            )
            
            uvicorn.run(
                starlette_app, 
                host=host, 
                port=port,
                log_level="debug" if settings.MCP_DEBUG else settings.LOG_LEVEL.lower()
            )
