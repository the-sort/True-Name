"""
Unit test for shop tool
"""
import pytest
import pygame
from tools.shop import CShop
from tools.player import CPlayer

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def screen():
    """
    Initializing screen
    """
    display = pygame.display.set_mode((10,10))
    return display



@pytest.fixture
def shops():
    """
    Initializing shops
    """
    r_shop = CShop(CPlayer("tests/profiles/rich_player.txt"), 10)
    p_shop = CShop(CPlayer("tests/profiles/poor_player.txt"), 10)
    o_shop = CShop(CPlayer("tests/profiles/one_shot_player.txt"), 10)
    return r_shop, p_shop, o_shop



def test_display(shops, screen):
    """
    Unit test checks for display metod presence
    """
    shop, _, _ = shops
    display = screen

    try:
        shop.display(display)
    except ImportError:
        pytest.fail("Display table method is not Implemented")

def test_buy(shops):
    """
    Unit test for shoping
    """
    r_shop, p_shop, o_shop = shops
    assert r_shop.upgrade_health()
    assert r_shop.upgrade_health()
    assert r_shop.upgrade_health()
    assert r_shop.upgrade_health()
    assert r_shop.upgrade_health()

    assert not p_shop.upgrade_health()

    assert o_shop.upgrade_health()
    assert not o_shop.upgrade_health()

#RESTRORING TEST DATA
TO_SAVE = "100\n50"
with open("tests/profiles/one_shot_player.txt", mode = "w", encoding = "utf-8") as f:
    f.write(TO_SAVE)
TO_SAVE = "1000\n0"
with open("tests/profiles/poor_player.txt", mode = "w", encoding = "utf-8") as f:
    f.write(TO_SAVE)
TO_SAVE = "100\n999999999999"
with open("tests/profiles/rich_player.txt", mode = "w", encoding = "utf-8") as f:
    f.write(TO_SAVE)
