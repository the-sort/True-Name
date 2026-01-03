"""
Unit test for slider tool
"""
import pygame
import pytest
from tools.slider import CSlider

screen = pygame.display.set_mode((10,10))

slider_t = CSlider(screen, 0, 0, active = True)
slider_f = CSlider(screen, 0, 0, active = False)

def test_activity():
    """
    Unit test for active method
    """
    assert slider_t.is_active()
    assert not slider_f.is_active()

    slider_t.deactivate()
    slider_f.activate()

    assert not slider_t.is_active()
    assert slider_f.is_active()

    slider_t.deactivate()
    slider_f.deactivate()

    assert not slider_t.is_active()
    assert not slider_f.is_active()

    slider_t.activate()
    slider_t.activate()
    assert slider_t.is_active()

def test_display():
    """
    Unit test for display method
    """
    try:
        slider_t.display_slider(0, 0)
    except ImportError:
        pytest.fail("Display table method is not Implemented")
