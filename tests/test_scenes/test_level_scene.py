"""
Unit tests related to level scene
"""
import pytest
import pygame
from scenes.level import CLevel
from scenes.scene_manager import CSceneManager

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def level() -> CLevel:
    """
    Initializing level scene
    """
    return CLevel(
        manager = CSceneManager(),
        difficultie = "EASY"
    )

def test_display(level):
    """
    Unit test for checking display metod pressence
    """
    t_level = level

    try:
        t_level.display(0)
        assert True
    except ImportError:
        pytest.fail("Display metod is missing")
