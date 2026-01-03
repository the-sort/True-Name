"""
Module for wraping and managing scenes
"""
from scenes.menu import CMenu
from scenes.level import CLevel
from scenes.start import CStart
from scenes.summary import CSummary
from tools.player import CPlayer


class CSceneManager():
    """
    Scene Manager class
    """
    def __init__(self, testing = False):
        self.scene = None
        self.player = CPlayer()

        self.__testing = testing

    def change_scene(self, manager, scene, difficultie = None):
        """
        Method for changing scene
        """
        del self.scene

        if scene != "START" and not self.__testing:
            self.player.save()

        match scene:
            case "EASY":
                self.scene = CLevel(manager, "EASY")
                return "EASY"
            case "MEDIUM":
                self.scene = CLevel(manager, "MEDIUM")
                return "MEDIUM"
            case "HARD":
                self.scene = CLevel(manager, "HARD")
                return "HARD"
            case "MENU":
                self.scene = CMenu(manager)
                return "MENU"
            case "START":
                self.scene = CStart(manager)
                return "START"
            case "VICTORY":
                self.scene = CSummary(manager, True, difficultie)
                return "VICTORY"
            case "LOOSE":
                self.scene = CSummary(manager, False, difficultie)
                return "LOOSE"
            case _:
                raise ValueError("Given scene does not exist")

if __name__ == "__main":
    ...
