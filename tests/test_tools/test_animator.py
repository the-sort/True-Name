"""
Unit tests for animator tool
"""
import pytest
import pygame
from tools.animator import CAnimations

screen = pygame.display.set_mode((10, 10))
animator = CAnimations("assets/wiz_idle")

def test_player():
    """
    Unit test for checking display metod presence
    """
    try:
        animator.play(screen, 0, (0, 0))
        assert True
    except ImportError:
        pytest.fail("Display metod is missing")

def test_getters():
    """
    Unit test for getter metods
    """

    img = pygame.image.load("assets/wiz_idle/idle_1.png")

    assert animator.get_keyframe() is not None

    assert animator.get_rect() is not None
    assert animator.get_rect() == img.get_rect()
