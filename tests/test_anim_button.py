"""
Unit tests for anim_button
"""
import pytest
import pygame
from tools.anim_button import CAnimButton, CAnimations

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


screen = pygame.display.set_mode((10, 10))
anim_button = CAnimButton(
                pos = (0, 0),
                idle = CAnimations("assets/wiz_idle"),
                hovered = CAnimations("assets/wiz_hover"),
                pressed = CAnimations("assets/wiz_pres"),
                on_press = pressed,
                on_release = released
)

anim_button1 = CAnimButton(
                pos = (0, 0),
                idle = CAnimations("assets/wiz_idle")
)

def test_button():
    """
    Unit test for button pressing and releasing
    """
    assert not anim_button.state()
    assert anim_button.released(pressed = True) == "Button was pressed"
    assert anim_button.state()
    assert anim_button.released(pressed = True) is None

    assert anim_button.released(pressed = False) is None
    assert anim_button.state()

    assert anim_button.released(pressed = True) == "Button was released"
    assert not anim_button.state()
    assert anim_button.released(pressed = True) is None

def test_clean_up():
    """
    Unit test for anim_button pressing and realising clean_up
    """
    anim_button.clean()
    anim_button.make_idle()

    assert anim_button.released(pressed = True) is None

    assert anim_button.released(pressed = False) is None

    assert anim_button.released(pressed = True) is None



def test_pos():
    """
    Unit test for procesing anim_button postion
    """
    assert anim_button.postion() == (0, 0)

    anim_button.move((33, 89))
    assert anim_button.postion() != (0, 0)
    assert anim_button.postion() == (33, 89)

def test_size():
    """
    Unit test for size related metods
    """
    assert anim_button.width("idle") == 384
    assert anim_button.height("idle") == 500

    assert anim_button.width("hovered") == 384
    assert anim_button.height("hovered") == 500

    assert anim_button.width("pressed") == 538
    assert anim_button.height("pressed") == 700

    try:
        assert anim_button.width("idle") == 384
        assert anim_button.height("idle") == 500
    except ValueError:
        pytest.fail("Invalid exception thrown")

    try:
        anim_button1.width("hovered")
        anim_button1.height("hovered")

        pytest.fail("No exception was caught")
    except ValueError:
        assert True

def test_display():
    """
    Unit test for pressence of display metod
    """
    try:
        anim_button.display(screen, 0, 0, delta_time = 0)
    except ImportError:
        pytest.fail("Ivalid exception raised")

    try:
        anim_button.display(screen, 0, 0, delta_time = 0)
        assert True
    except ValueError:
        pytest.fail("Ivalid exception raised delta is required")
