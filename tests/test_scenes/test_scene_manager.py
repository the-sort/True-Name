"""
Unit tests related to scene manager
"""
import pytest
import pygame
from scenes.scene_manager import CSceneManager

manager = CSceneManager(testing = True)

@pytest.fixture(scope = "session", autouse = True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()


def test_change_scene():
    """
    Unit tests related to change scene metod
    """
    assert manager.change_scene(manager, "EASY") == "EASY"
    assert manager.change_scene(manager, "MEDIUM") == "MEDIUM"
    assert manager.change_scene(manager, "HARD") == "HARD"
    assert manager.change_scene(manager, "MENU") == "MENU"
    assert manager.change_scene(manager, "START") == "START"
    assert manager.change_scene(manager, "VICTORY", "EASY") == "VICTORY"
    assert manager.change_scene(manager, "LOOSE", "MEDIUM") == "LOOSE"

    try:
        manager.change_scene(manager, "SLOVAKIA")
        pytest.fail("No exception raised to invalid Scene")
    except ValueError:
        assert True
