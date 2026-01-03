"""
Unit test for Evaluator tool
"""
from tools.evaluator import CEvaluator

evaluator_1 = CEvaluator("tests/profiles/photo_set_1/", False)
evaluator_2 = CEvaluator("tests/profiles/photo_set_2/", False)
evaluator_empty = CEvaluator("tests/profiles/photo_set_empty/", False)

def test_evaluator_1():
    """
    Unit test for evaluator
    """
    res = evaluator_1.make_string(False)

    assert res == "PYTHON"
    assert res != "C++"

def test_evaluator_2():
    """
    Unit test for evaluator
    """
    res = evaluator_2.make_string(False)
    assert res == "BLEEDITOUT"
    assert res != "IN THE END"

def test_evaluator_empty():
    """
    Unit test for evaluator
    """
    res = evaluator_empty.make_string(False)
    assert res == ""
    assert res != "Guido van Rossum"
    assert res != "LINKIN PARK"
