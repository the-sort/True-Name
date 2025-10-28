"""Path Finder MCP Server assignment."""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import FastMCPError

from utils import DISTRICTS_FOLDER, HOST, PORT, TRANSPORT, find_best_path_bfs, NameNotInDistrictError, Node, load_district

# Create an MCP server
server = FastMCP("Path Finder", host=HOST, port=PORT)

def check_availability(district_name):
    """Checks if resource is available"""
    try:
        open(f"{DISTRICTS_FOLDER}/{district_name}.txt", "r", encoding="utf-8")
        return True
    except FileNotFoundError:
        return f"{DISTRICTS_FOLDER}/{district_name}.txt does not exist"
    except PermissionError:
        return f"Inssuficient permision to acces {DISTRICTS_FOLDER}/{district_name}.txt"

def validate_district_name(district_name):
    """ Valid district name contains only:
        alphanumerical values, spaces, single quotes and underscores"""
    for char in district_name:
        if not  (   char.isalnum()  or
                    char == "'"     or
                    char == "_"
                ):
            return False
    return True


# Prompt
@server.prompt()
def sample_prompt():
    """Creates a new prompt to find best path."""
    return "Find best path from Waffles to Storage in the Maple district."

# Resource
@server.resource("district://{district_name}")
def district_resource(district_name):
    """"Get a desired district resource."""
    if isinstance(check_availability(district_name), str):
        return
    if not validate_district_name(district_name):
        return

    return ...

# Tool
def find_best_path_tool(building_from, building_to, district_name):
    return ...

if __name__ == "__main__":
    server.run(transport=TRANSPORT)
