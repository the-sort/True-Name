"""
Unit test for player tool
"""
import pytest
from tools.player import CPlayer

player = CPlayer("tests/profiles/model_player.txt")

def test_health():
    """
    Unit test for health related methods
    """
    assert player.health() == 100

    player.deacrease_health(-50)
    assert player.health() == 50

    player.deacrease_health(50)
    assert player.health() == 50

    player.deacrease_health(0)
    assert player.health() == 50

    player.increase_health(10)
    assert player.health() == 60

    player.increase_health(-10)
    assert player.health() == 60

    player.increase_health(0)
    assert player.health() == 60

    player.heal_to_full()
    assert player.health() == 100

    player.increase_full_health(100)
    assert player.health() == 100
    assert  player.full_health() == 200

    player.heal_to_full()
    assert player.health() == 200

def test_coin():
    """
    Unit test for coin related methods
    """
    assert player.coins() == 100

    player.substract_coins(50)
    assert player.coins() == 50

    try:
        player.substract_coins(-50)
        pytest.fail("Value Error not raised")
    except ValueError:
        assert player.coins() == 50

    try:
        player.substract_coins(0)
        pytest.fail("Value Error not raised")
    except ValueError:
        assert player.coins() == 50


    player.add_coins(50)
    assert player.coins() == 100

    try:
        player.add_coins(-50)
        pytest.fail("Value Error not raised")
    except ValueError:
        assert player.coins() == 100

    try:
        player.add_coins(0)
        pytest.fail("Value Error not raised")
    except ValueError:
        assert player.coins() == 100

#RESTORING TEST DATA
TO_SAVE = "100\n100"
with open("tests/profiles/model_player.txt", mode = "w", encoding = "utf-8") as f:
    f.write(TO_SAVE)
