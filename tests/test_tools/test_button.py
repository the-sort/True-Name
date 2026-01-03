"""
Unit tests for button module
"""
import pygame
import pytest
from tools.button import CButton

def pressed():
    """
    Function for button press
    """
    return "Button was pressed"


def released():
    """
    Function for button release
    """
    return "Button was released"

screen = pygame.display.set_mode((1000, 1000))

button = CButton(
            position = (0, 0),
            idle = "assets/wiz_idle/idle_1.png",
            hovered = "assets/wiz_hover/hover_1.png",
            pressed = "assets/wiz_pres/pressed_1.png",
            on_press = pressed,
            on_release = released
)

button1 = CButton(
            position = (0, 0),
            idle = "assets/wiz_idle/idle_1.png",
)

def test_button():
    """
    Unit test for button pressing and releasing
    """
    assert not button.state()
    assert button.released(pressed = True) == "Button was pressed"
    assert button.state()
    assert button.released(pressed = True) is None

    assert button.released(pressed = False) is None
    assert button.state()

    assert button.released(pressed = True) == "Button was released"
    assert not button.state()
    assert button.released(pressed = True) is None

def test_clean_up():
    """
    Unit test for button pressing and realising clean_up
    """
    button.clean()
    button.make_idle()

    assert button.released(pressed = True) is None

    assert button.released(pressed = False) is None

    assert button.released(pressed = True) is None



def test_pos():
    """
    Unit test for procesing button postion
    """
    assert button.postion() == (0, 0)

    button.move((15, 13))
    assert button.postion() != (0, 0)
    assert button.postion() == (15, 13)

def test_size():
    """
    Unit test for size related metods
    """
    assert button.width("idle") == 384
    assert button.height("idle") == 500

    assert button.width("hovered") == 384
    assert button.height("hovered") == 500

    assert button.width("pressed") == 538
    assert button.height("pressed") == 700

    try:
        assert button.width("idle") == 384
        assert button.height("idle") == 500
    except ValueError:
        pytest.fail("Invalid exception thrown")

    try:
        button1.width("hovered")
        button1.height("hovered")

        pytest.fail("No exception was caught")
    except ValueError:
        assert True

def test_display():
    """
    Unit test for pressence of display metod
    """
    try:
        button.display(screen, 0, 0)
    except ImportError:
        pytest.fail("Ivalid exception raised")

    try:
        button.display(screen, 0, 0, delta_time = 10)
        pytest.fail("No exception was raised")
    except ValueError:
        assert True
