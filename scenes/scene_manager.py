"""
Module for wraping and managing scenes
"""
from scenes.menu import CMenu
from scenes.level import CLevel
from tools.player import CPlayer


class CSceneManager():
    """
    Scene Manager class
    """
    def __init__(self):
        self.scene = None
        self.player = CPlayer()

    def change_scene(self, manager, scene):
        """
        Method for changing scene
        """
        del self.scene
        self.player.save()
        match scene:
            case "EASY":
                self.scene = CLevel(manager, "EASY")
            case "MEDIUM":
                self.scene = CLevel(manager, "MEDIUM")
            case "HARD":
                self.scene = CLevel(manager, "HARD")
            case "MENU":
                self.scene = CMenu(manager)

if __name__ == "__main":
    ...
