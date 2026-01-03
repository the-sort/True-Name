"""
Unit tests related to menu scene
"""
import pytest
import pygame
from scenes.menu import CMenu
from scenes.scene_manager import CSceneManager

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def start() -> CMenu:
    """
    Initializing start scene
    """
    return CMenu(manager = CSceneManager())

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
