"""Path Finder MCP Server assignment."""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import FastMCPError

from utils import DISTRICTS_FOLDER, HOST, PORT, TRANSPORT, find_best_path_bfs, NameNotInDistrictError, Node

# Create an MCP server
server = FastMCP("Path Finder", host=HOST, port=PORT)

def check_availability(district_name):
    """Checks if resource is available, when true returns opened file"""
    try:
        file = open(f"{DISTRICTS_FOLDER}/{district_name}.txt", "r", encoding="utf-8")
        return file
    except FileNotFoundError:
        return False
    except PermissionError:
        return False

def validate_district_name(district_name):
    """ Valid district name contains only:
        alphanumerical values, spaces, single quotes and underscores"""
    for char in district_name:
        if not  (   char.isalnum()  or
                    char == "'"     or
                    char == "_"
                ):
            raise FastMCPError("District name contains invalid characters")


# Prompt
@server.prompt()
def sample_prompt():
    """Creates a new prompt to find best path."""
    return "Find best path from Waffles to Storage in the Maple district."

# Resource
@server.resource("district://{district_name}")
def district_resource(district_name):
    """"Get a desired district resource."""
    content = ""
    validate_district_name(district_name)
    if not(file:=check_availability(district_name)):
        return
    for line in file.readlines():
        content += line
    return content

# Tool
def find_best_path_tool(building_from, building_to, district_name):
    return ...

if __name__ == "__main__":
    server.run(transport=TRANSPORT)
