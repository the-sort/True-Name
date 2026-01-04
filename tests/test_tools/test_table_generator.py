"""
Unit test for table generator tool
"""
import pytest
import pygame
from tools import table_generator
from tools.utils import CDificulties


@pytest.fixture(scope = "session", autouse = True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

screen = pygame.display.set_mode((10,10))
easy_table = table_generator.CTable(screen, CDificulties("EASY"), "ENG")
medium_table = table_generator.CTable(screen, CDificulties("MEDIUM"), "ENG")
hard_table = table_generator.CTable(screen, CDificulties("HARD"), "ENG")


def test_retrictions():
    """
    Unit test checking max and min len
    """
    assert table_generator.MAX_WORD_LEN == 9
    assert table_generator.MIN_WORD_LEN == 3


def test_display():
    """
    Unit test checks for display metod presence
    """
    try:
        easy_table.display_table()
        assert True
    except ImportError:
        pytest.fail("Display table method is not Implemented")

def count_cols(table):
    """
    Helper function for counting cols in table
    """
    cols = 0
    for _ in table[0]:
        cols += 1
    return cols

def test_table():
    """
    Unit test for table
    """
    assert len(easy_table.table()) == 5
    assert len(medium_table.table()) == 6
    assert len(hard_table.table()) == 12

    assert count_cols(easy_table.table()) == 6
    assert count_cols(medium_table.table()) == 8
    assert count_cols(hard_table.table()) == 16

def test_solution():
    """
    Unit test for Soultion
    """
    assert easy_table.solution() != "!Happy!"
    assert medium_table.solution() != "!New!"
    assert hard_table.solution() != "!Year!"

    assert easy_table.solution() is not None
    assert medium_table.solution() is not None
    assert hard_table.solution() is not None
