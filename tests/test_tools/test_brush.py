"""
Unit test for brush tool
"""
from tools.brush import CBrush

brush = CBrush()

def test_lifting():
    """
    Unit test related to lifting brush
    """
    assert not brush.is_down()

    brush.down()
    assert brush.is_down()

    brush.up()
    assert not brush.is_down()

    brush.up()
    assert not brush.is_down()
