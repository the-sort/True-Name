"""
This script runs main game_loop
"""
import pygame
from scenes.scene_manager import CSceneManager
from scenes.menu import CMenu

if __name__ == "__main__":

    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    clock = pygame.time.Clock()

    manager = CSceneManager()
    manager.change_scene(CMenu(manager))

    while RUNNING:
        RUNNING = manager.scene.display(DELTA_TIME)

        pygame.display.flip()
        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
