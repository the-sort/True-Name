"""
Unit tests related to menu scene
"""
import pytest
import pygame
from scenes.menu import CMenu
from scenes.scene_manager import CSceneManager

@pytest.fixture(scope = "session", autouse = True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def menu() -> CMenu:
    """
    Initializing menu scene
    """
    return CMenu(manager = CSceneManager())

def test_display(menu):
    """
    Unit test for checking display metod pressence
    """
    t_menu = menu

    try:
        t_menu.display(0)
        assert True
    except ImportError:
        pytest.fail("Display metod is missing")
