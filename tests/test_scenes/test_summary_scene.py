"""
Unit tests related to summary scene
"""
import pytest
import pygame
from scenes.summary import CSummary
from scenes.scene_manager import CSceneManager

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """
    Initializing pygame
    """
    pygame.font.init()

@pytest.fixture
def summaries():
    """
    Initializing summaries
    """
    e_summary = CSummary(
            manager = CSceneManager(),
            completed = True,
            difficultie = "EASY"
    )

    m_summary = CSummary(
                manager = CSceneManager(),
                completed = True,
                difficultie = "MEDIUM"
    )

    h_summary = CSummary(
                manager = CSceneManager(),
                completed = True,
                difficultie = "HARD"
    )
    return e_summary, m_summary, h_summary


def test_display(summaries):
    """
    Unit test for checking display metod pressence
    """
    summarie, _, _= summaries
    try:
        summarie.display(0)
        assert True
    except ImportError:
        pytest.fail("Display metod is missing")

def test_interactions(summaries):
    """
    Unit test for interactions
    """
    e_summary, m_summary, h_summary = summaries
    assert e_summary.restart_level("EASY") == "EASY"
    assert m_summary.restart_level("MEDIUM") == "MEDIUM"
    assert h_summary.restart_level("HARD") == "HARD"

    assert e_summary.go_to_menu() == "MENU"
