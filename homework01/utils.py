"""This module serves helper functions for finding shortest path using the BFS algorithm."""


# Public constants
HOST: str = "localhost"
PORT: int = 8000
TRANSPORT: str = "streamable-http"
DISTRICTS_FOLDER: str = "districts"

# Public classes
class NameNotInDistrictError(Exception):
    """Exception raised when a field name does not exist in the district. Should describe the name that was not found."""
    pass

class Node:
    """A node within the 2D district graph. Expects positions in (y, x) format."""
    def __init__(self, name: str, position: tuple[int, int]):
        self.name = name
        self.position = position
        self.walkable = self._is_walkable()
        self.adjacent = []
        self.visited = False
        self.distance = float("inf")
        self.previous = None

    def is_intersection(self) -> bool:
        """Check if the name is an intersection of two avenues."""
        l = self.name.split("/")
        # Or is a intersection of two Avenues
        if len(l) == 2 and len(l[0]) == 3 and len(l[1]) == 3:
            return True
        return False

    def _is_walkable(self) -> bool:
        """Check if the name is walkable (an avenue or an intersection of avenues)."""
        if self.name[-4:] == " Ave":
            return True
        return self.is_intersection()

# Public functions
def load_district(district_name: str) -> list[list[str]]:
    """Load district file into string."""
    with open(f"{DISTRICTS_FOLDER}/{district_name}.txt", "r", encoding="utf-8") as file:
        district = eval(file.read(), {"__builtins__": None}, {})  # Safer eval
    return district

def find_best_path_bfs(building_from: str, building_to: str, district_name: str) -> tuple[list[list[Node]], list[Node]]:
    """Find the best path between two buildings in a given district using BFS algorithm."""
    # Prepare district (Index like [y][x])
    string_array: list[list[str]] = load_district(district_name)
    node_array: list[list[Node]] = _get_node_array(string_array)
    _link_nodes(node_array)
    path: list[Node] = _bfs(node_array, building_from, building_to)
    return node_array, path

# Protected functions
def _get_node_array(district: list[list[str]]) -> list[list[Node]]:
    """Convert string district into a 2D array of Nodes."""
    node_array = [None for _ in range(len(district))]
    for y, old_row in enumerate(district):
        row = [None for _ in range(len(old_row))]
        for x, field_name in enumerate(old_row):
            row[x] = Node(field_name, (y, x))
        node_array[y] = row
    return node_array

def _iter_2d_arr(arr: list[list[Node]]):
    """Syntactic sugar: Iterator over 2D array yielding (y, x) positions."""
    for y, row in enumerate(arr):
        for x in range(len(row)):
            yield y, x

def _link_nodes(node_array: list[list[Node]]) -> None:
    """Link nodes in the 2D array to their directly walkable adjacent nodes. Links pairs: avenue-avenue and avenue-building (including building-avenue)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for y, x in _iter_2d_arr(node_array):
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            if 0 <= ny < len(node_array) and 0 <= nx < len(node_array[ny]):
                if node_array[y][x].walkable or node_array[ny][nx].walkable:
                    node_array[y][x].adjacent.append(node_array[ny][nx])

def _get_node(node_array: list[list[Node]], name: str) -> Node:
    """Get node by name from 2D array."""
    for y, x in _iter_2d_arr(node_array):
        if node_array[y][x].name == name:
            return node_array[y][x]
    raise NameNotInDistrictError(f"Node with name {name} not found within the district.")

def _reconstruct_path(end_node: Node, solution_found: bool) -> list[Node]:
    """Reconstruct path from end node to start node. Returns list of (y, x) positions."""
    if not solution_found:
        return []
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = current.previous
    path.reverse()
    return path

def _bfs(node_array: list[list[Node]], start_name: str, end_name: str) -> list[Node]:
    """Breadth-First Search to find the shortest path."""
    # Variables
    start_node = _get_node(node_array, start_name)
    end_node = _get_node(node_array, end_name)
    queue = [start_node]
    start_node.visited = True
    start_node.distance = 0

    # BFS Loop
    solution_found = False
    while queue:
        current_node = queue.pop(0)
        if current_node == end_node:
            break
        for neighbor in current_node.adjacent:
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.distance = current_node.distance + 1
                neighbor.previous = current_node
                if neighbor.walkable:
                    queue.append(neighbor)
                if neighbor == end_node:
                    solution_found = True
                    break
    return _reconstruct_path(end_node, solution_found)
