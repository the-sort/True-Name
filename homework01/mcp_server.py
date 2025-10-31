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

def validate_avenue(avenue):
    """Valid avenue contains only:
        alphanumerical values and is in format:\n
        1)"XXX Ave"\n
        2"XXX/YYY"
    """
    for char in avenue[:3]:
        if not char.isalnum() :
            raise FastMCPError("Avenue prefix contains non alphanumerical values")
    if avenue[3] == " " :
        if "Ave" in avenue[-3:-1]:
            raise FastMCPError("In format 'XXX Ave' Ave suffix is missing")
    elif avenue[3] == "\\" :
        for char in avenue[:3]:
            if not char.isalnum() :
                raise FastMCPError("In format 'XXX/YYY' suffix contains non alphanumerical values")
    raise FastMCPError("None of valid formats were satysfied")

def avenue_or_building(param):
    """Differing between building or avenue"""
    if len(param) >= 7 :
        raise FastMCPError("avenue or building name is too long")
    if param[3] == " " or param[3] == "\\":
        validate_avenue(param)
    else :
        validate_building_name(param)


def format_path(path : list[Node]) -> str:
    """Reconstructs the path and returns in proper format"""
    out = "Found path:\n    "
    for node in path:
        if node == path[-1] :
            out += node.name
            break
        out += f"{node.name} → "
    out +="\n"
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
    return out

#   width = len(parsed_file[0]) * 10 - 1
def create_minimap(building_from, building_to, district_name):
    """Parses district file, creates minimap and highlights from/to buildings"""
    out = ""
    parsed_file = parse_file(district_name)
    am_partitions = len(parsed_file[0]) - 1
    partion_up = ("─" * 9) + "┬"
    partion_middle = ("─" * 9) + "┼"
    partion_down = ("─" * 9) + "┴"
    suffix_up = ("─" * 9) + "┐" + "\n"
    suffix_middle = ("─" * 9) + "┤" + "\n"
    suffix_down = ("─" * 9) + "┘" + "\n"
    out += "Minimap:\n"
    out += " " * 4 + "┌" + partion_up * am_partitions + suffix_up
    for line in parsed_file:
        out += " " * 4 + "│"
        for word in line:
            if word == building_from or word == building_to :
                out += ">" + word + "<" "│"
            else :
                out += " " + word + " " "│"
        out += "\n"
        if line == parsed_file[-1] :
            break
        out += " " *4 + "├" +partion_middle * am_partitions + suffix_middle
    out += " " * 4 + "└" + partion_down * am_partitions + suffix_down
    out += "\n"
    return out


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
@server.tool()
def find_best_path_tool(building_from, building_to, district_name):
    """ Find the optimal path between two buildings in a district and 
        return both the path and a minimap showing the path steps.
    """
    out : str = ""
    validate_building_name(building_from)
    validate_building_name(building_to)
    validate_district_name(district_name)
    try:
        path : tuple = find_best_path_bfs(building_from, building_to, district_name)
    except NameNotInDistrictError as e:
        raise FastMCPError(e) from e
    out += format_path(path[1])
    out += create_minimap(building_from, building_to, district_name)
    out += "Instructions:\n"
    return out



if __name__ == "__main__":
    server.run(transport=TRANSPORT)
