"""Path Finder MCP Server assignment."""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import FastMCPError

from utils import DISTRICTS_FOLDER, HOST, PORT, TRANSPORT, find_best_path_bfs, NameNotInDistrictError, Node

# Create an MCP server
server = FastMCP("Path Finder", host=HOST, port=PORT)

# Prompt
def sample_prompt():
    return ...

# Resource
def district_resource(district_name):
    return ...

# Tool
def find_best_path_tool(building_from, building_to, district_name):
    return ...

if __name__ == "__main__":
    server.run(transport=TRANSPORT)
