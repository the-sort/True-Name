"""
Unit tests for attempts tool
"""
import pygame
import pytest
from tools.attempts import CAttempts

screen = pygame.display.set_mode((10, 10))

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

attempts = CAttempts(screen)

def test_display():
    """
    Unit test for checking presence of display metod
    """
    try:
        attempts.display_attempts(0, 0)
        assert True
    except ImportError:
        pytest.fail("Display Metod missing")
