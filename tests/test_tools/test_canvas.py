"""
Unit test for Canvas tool
"""
import os
import pygame
import pytest
from tools.canvas import CCanvases

PATH = "tests/profiles/canvases/"
canvas = CCanvases(10, PATH)
display = pygame.display.set_mode((10, 10))

def test_display():
    """
    Unit test for display metod presence
    """
    try:
        canvas.display_canvases(display, 0, 0)
    except ImportError:
        pytest.fail("Display method is missing")

def test_size():
    """
    Unit test for checking canvas size
    """
    assert canvas.size_of_one() == (175, 175)
    assert canvas.size_of_one() != (0, 0)

def test_save():
    """
    Unit test for saving metod
    """
    files = [file for file in os.listdir(PATH)]
    assert not files

    canvas.save()

    files = [file for file in os.listdir(PATH)]
    assert len(files) == 10

    #files clean_up
    for file in files:
        os.remove(PATH + file)
