"""
Unit tests related to start scene
"""
import pytest
import pygame
from scenes.start import CStart
from scenes.scene_manager import CSceneManager

PATH = "tests/profiles/new_player.txt"

@pytest.fixture(scope = "session", autouse = True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def start() -> CStart:
    """
    Initializing start scene
    """
    return CStart(
        manager = CSceneManager(),
        path = PATH
    )

def test_display(start):
    """
    Unit test for checking display metod pressence
    """
    t_start = start

    try:
        t_start.display(0)
        assert True
    except ImportError:
        pytest.fail("Display metod is missing")

def test_go_to_menu(start):
    """
    Unit test for go_to_menu interaction
    """
    t_start = start

    assert t_start.scene_to_menu()  == "MENU"

def test_new_game(start):
    """
    Unit test for new game reset
    """
    t_start = start

    t_start.accept()

    with open(PATH, mode = "r", encoding = "utf-8") as file:
        stats = [int(stat) for stat in file]

        assert stats[0] == 200
        assert stats[1] == 0
