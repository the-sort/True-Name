"""
Module for wraping and managing scenes
"""
class CSceneManager():
    """
    Scene Manager class
    """
    def __init__(self):
        self.scene = None

    def change_scene(self, scene):
        """
        Method for changing scene
        """
        self.scene = scene

if __name__ == "__main":
    ...
