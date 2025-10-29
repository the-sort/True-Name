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
        alphanumerical values, spaces, single quotes and underscores
    """
    for char in district_name:
        if not  (   char.isalnum()  or
                    char == "'"     or
                    char == "_"
                ):
            raise FastMCPError("District name contains invalid characters")

def validate_building_name(building_name):
    """ Valid district building name contains only:
        alphanumerical values and spaces
    """
    am_of_chars = 0
    for char in building_name:
        if am_of_chars >= 7:
            raise FastMCPError("Building name contains more than 7 characters")
        if not (char.isalnum()  or
                char == "'"
                ):
            raise FastMCPError("Building name contains invalid characters")
        am_of_chars += 1

def format_path(path : list[Node]) -> str:
    """Reconstructs the path and returns in proper format"""
    out = "Found path:\n    "
    for node in path:
        if node == path[-1] :
            out += node.name
            break
        out += f"{node.name} -> "
    return out

def parse_file(district_name) -> list[list[str]]:
    """Removes first and last line and parse all lines"""
    out : list[list[str]] = []
    parsed_line : list[str] = ["1","1","1"]
    if not (file := check_availability(district_name)) :
        return None
    lines = file.readlines()
    lines = lines[1:-1]
    for line in lines:
        line = line.removeprefix("    [")
        line = line.removesuffix("],\n")
        parsed_line = line.split(", ")
        it = 0
        for word in parsed_line :
            word = word.removeprefix("\"")
            parsed_line[it] = word.removesuffix("\"")
            it += 1
        out.append(parsed_line)
    for word in out:
        print(word)
    return out

# def create_minimap(district_name, building_from, building_to):
#     """Parses district file, creates minimap and highlights from/to buildings"""
#     parsed_file = parse_file(district_name)
#     width = parsed_file

#     out = "Minimap:\n"



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
        return None
    for line in file.readlines():
        content += line
    return content

# Tool
def find_best_path_tool(building_from, building_to, district_name):
    """ Find the optimal path between two buildings in a district and 
        return both the path and a minimap showing the path steps.
    """
    out : str = ""
    validate_building_name(building_from)
    validate_building_name(building_to)
    validate_district_name(district_name)
    if not(file:=check_availability(district_name)):
        return None
    path : tuple = find_best_path_bfs(building_from, building_to, district_name)
    out += format_path(path[1])
    return out



if __name__ == "__main__":
    server.run(transport=TRANSPORT)
