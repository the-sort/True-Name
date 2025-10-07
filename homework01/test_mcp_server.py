"""Private MCP server tests. Requires pytest-asyncio."""

import ast
from pathlib import Path
import inspect
import pytest
from pylint import lint, reporters
from mcp.types import Prompt
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.fastmcp.exceptions import FastMCPError

import mcp_server


# Constants
DISTRICT_NAMES = ["Maple", "Greenwood"]
DISTRICTS_FOLDER_NAME = "districts"
PROMPT_FN_NAME = "sample_prompt"
PROMPT_DESCRIPTION = "Creates a new prompt to find best path."
RESOURCE_FN_NAME = "district_resource"
TOOL_FN_NAME = "find_best_path_tool"
ALLOWED_IMPORTS = ("mcp", "utils", "re")


# Tests
@pytest.fixture(scope="session", name="linter")
def fixture_linter() -> None:
    """ Use pylint to test codestyle for src file. """
    src_file = inspect.getfile(mcp_server)
    rep = reporters.CollectingReporter()
    # disabled warnings:
    # C0301 line too long
    # C0103 variables name (does not like shorter than 2 chars)
    # W0123 eval used (useful when loading districts)
    r = lint.Run(['--disable=C0301,C0103,W0123', '-sn', src_file], reporter=rep, exit=False)
    return r.linter

@pytest.mark.parametrize("limit", range(3, 11))
def test_codestyle_score(linter: lint.pylinter.PyLinter, limit: int) -> None:
    """ Evaluate codestyle for different thresholds. """
    score = linter.stats.global_note
    assert score >= limit, f"Codestyle score {score} is lower than {limit}"

def get_imports(source=None, source_file=None, modules=None, names=None, recursive=False) -> None:
    """ Traverse source and pick imports. """
    if source is None and source_file is None:
        raise ValueError('At least source or source_file must not be None.')

    if source is not None:
        a = ast.parse(source)
    else:
        a = ast.parse(Path(source_file).read_text(encoding='utf-8'))

    if modules is None:
        modules = []
    if names is None:
        names = []

    for node in ast.walk(a):
        if isinstance(node, ast.ImportFrom):
            modules += [node.module]
            names += [f'{node.module}.{item.name}' for item in node.names]

        if isinstance(node, ast.Import):
            modules += [item.name for item in node.names]

    # Fake recursion thanks to the appending to the end of modules list,
    # the newly explored imports will be processed in the same for-loop
    if recursive:
        for m in modules:
            if Path(f'{m}.py').exists():
                get_imports(
                    source=None,
                    source_file=f'{m}.py',
                    modules=modules,
                    names=names,
                    recursive=False
                )
    return modules, names

def test_no_extra_imports_allowed() -> None:
    """Only import from the mcp library and utils."""
    src_file = inspect.getfile(mcp_server)
    modules, _ = get_imports(source_file=src_file, recursive=True)

    # Iterate through all imports
    for module in modules:
        first_part = module.split(".")[0]
        err_msg = f"Import from non-allowed library: {module}. Allowed: {ALLOWED_IMPORTS}"
        assert first_part in ALLOWED_IMPORTS, err_msg

@pytest.mark.asyncio
async def test_prompt_decorator() -> None:
    """Check that the prompt decorator is correctly set"""
    prompts: list[Prompt] = await mcp_server.server.list_prompts()
    correct = False
    for prompt in prompts:
        if prompt.name == PROMPT_FN_NAME and prompt.description == PROMPT_DESCRIPTION:
            correct = True
            break
    assert correct, f"Prompt {PROMPT_FN_NAME} with correct signature was not found."

def test_resource_signature() -> None:
    """Checks basic properties of the resource function."""
    assert hasattr(mcp_server, RESOURCE_FN_NAME), f"Function {RESOURCE_FN_NAME} does not exist"
    func = mcp_server.__dict__[RESOURCE_FN_NAME]
    assert inspect.isfunction(func), f"{RESOURCE_FN_NAME} is not a function"
    sig = inspect.signature(func)
    assert len(sig.parameters) == 1, f"{RESOURCE_FN_NAME} should take one parameter"

@pytest.mark.asyncio
@pytest.mark.parametrize("district_name", DISTRICT_NAMES)
async def test_resource_input(district_name: str) -> None:
    """Checks varying values for resource function."""
    def load_district_file(district_name: str) -> str:
        """Load district file directly."""
        district_path = f"{DISTRICTS_FOLDER_NAME}/{district_name}.txt"
        with open(district_path, "r", encoding="utf-8") as file:
            return file.read()
    tested_results: list = await mcp_server.server.read_resource(f"district://{district_name}")
    tested_result: ReadResourceContents = tested_results[0]
    ground_truth = load_district_file(district_name)
    assert tested_result.content == ground_truth

@pytest.mark.asyncio
async def test_tool_decorator() -> None:
    """Check that the tool decorator is correctly set."""
    tools = await mcp_server.server.list_tools()
    correct = False
    for tool in tools:
        if tool.name == TOOL_FN_NAME:
            correct = True
            break
    assert correct, f"Tool {TOOL_FN_NAME} with correct signature was not found."

@pytest.mark.asyncio
@pytest.mark.parametrize("arguments, expected", [
    (
        {"building_from": "Waffles", "building_to": "Storage", "district_name": "Maple"},
        """\
Found path:
    Waffles → 1st Ave → 2nd Ave → 3rd Ave → 4th Ave → 5th Ave → 6th Ave → Storage
Minimap:
    ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
    │ Oak Ave │ 1st/Oak │ Oak Ave │ Oak Ave │ Oak/3rd │ Oak Ave │ Oak Ave │ XXXXXXX │ XXXXXXX │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │ 1st Ave │ XXXXXXX │ XXXXXXX │ 3rd Ave │ XXXXXXX │ XXXXXXX │ XXXXXXX │>Storage<│
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ Kungpao │ 1st Ave │ XXXXXXX │ XXXXXXX │ 3rd Ave │ XXXXXXX │   14    │   15    │   16    │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │ 1st Ave │ XXXXXXX │ XXXXXXX │ 3rd Ave │ XXXXXXX │   13    │ XXXXXXX │ XXXXXXX │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │    1    │>Waffles<│ XXXXXXX │   10    │   11    │   12    │ XXXXXXX │ XXXXXXX │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │    2    │ XXXXXXX │ XXXXXXX │    9    │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │    3    │ XXXXXXX │ XXXXXXX │    8    │ XXXXXXX │ XXXXXXX │ Brewery │ XXXXXXX │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ 2nd Ave │    4    │    5    │    6    │    7    │ 2nd Ave │ 2nd Ave │ 2nd Ave │ 2nd Ave │
    ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
    │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │ XXXXXXX │
    └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
Instructions:
    Copy the 'Found path' and 'Minimap' outputs to the user in Markdown.
"""
    ),
    (
        {"building_from": "House 3", "building_to": "House 5", "district_name": "Greenwood"},
        """\
Found path:
    House 3 → Bob Ave → House 5
Minimap:
    ┌─────────┬─────────┬─────────┐
    │ House 1 │ House 2 │>House 3<│
    ├─────────┼─────────┼─────────┤
    │ Bob Ave │    2    │    1    │
    ├─────────┼─────────┼─────────┤
    │ House 4 │>House 5<│ House 6 │
    ├─────────┼─────────┼─────────┤
    │ House 7 │ House 8 │ House 9 │
    └─────────┴─────────┴─────────┘
Instructions:
    Copy the 'Found path' and 'Minimap' outputs to the user in Markdown.
"""
    )
])
async def test_tool_input(arguments: dict[str, str], expected: str) -> None:
    """Check varying values for tool function."""
    result_text = mcp_server.__dict__[TOOL_FN_NAME](**arguments)
    assert result_text == expected, f"Tool {TOOL_FN_NAME} returned incorrect result"

@pytest.mark.parametrize("arguments", [
    {"building_from": "_5e2.,.", "building_to": "Storage", "district_name": "Maple"},
    {"building_from": "Waffles", "building_to": "NoExist", "district_name": "Maple"},
])
def test_tool_invalid_input(arguments: dict[str, str]) -> None:
    """Check invalid values for tool function."""
    with pytest.raises(FastMCPError):
        mcp_server.__dict__[TOOL_FN_NAME](**arguments)
