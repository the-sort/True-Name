"""
Unit test for Utils tool
"""
from PIL import Image
from tools import utils


easy = utils.CDificulties("EASY")
medium = utils.CDificulties("MEDIUM")
hard = utils.CDificulties("HARD")

blank = Image.open("assets/blank.png")
coin = Image.open("assets/coin.png")

def test_easy():
    """
    Unit test for easy difficultie
    """
    assert easy.difficultie() == "EASY"
    assert easy.cols() == 6
    assert easy.rows() == 5
    assert easy.scale() == 5
    assert easy.font_size() == 35
    assert easy.health_drain() == -0.25
    assert easy.reward() == 50

def test_medium():
    """
    Unit test for easy difficultie
    """
    assert medium.difficultie() == "MEDIUM"
    assert medium.cols() == 8
    assert medium.rows() == 6
    assert medium.scale() == 4
    assert medium.font_size() == 30
    assert medium.health_drain() == -0.5
    assert medium.reward() == 100

def test_hard():
    """
    Unit test for easy difficultie
    """
    assert hard.difficultie() == "HARD"
    assert hard.cols() == 16
    assert hard.rows() == 12
    assert hard.scale() == 2
    assert hard.font_size() == 15
    assert hard.health_drain() == -1
    assert hard.reward() == 200

def test_is_blank():
    """
    Unit test is_blank function
    """
    assert utils.is_blank(blank)
    assert not utils.is_blank(coin)

def test_percentage():
    """
    Unit test for percetange function
    """
    assert utils.percetage(100, 20) == 20
    assert utils.percetage(500, 50) == 250
    assert utils.percetage(150, 32) == 48
