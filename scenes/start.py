"""
Start_up menu 
"""
import pygame
from tools.button import CButton

SCREEN_W = 500
SCREEN_H = 500

class CStart():
    """
    Class for displaying and handling Start_up scene
    """
    def __init__(self, manager):
        self.__manager = manager
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))



        self.__new_game     = CButton(  position    = (0,0),
                                        idle        = "assets/start_up/new_game.png",
                                    )
        self.__continue     = CButton(  position    = (0, SCREEN_H // 2),
                                        idle        = "assets/start_up/continue.png",
                                    )


    def display(self, __delta_time):
        """
        Method for displaying Scene in Game_loop
        """
        self.__screen.fill((0,0,0))


        continue_looping = self.__event_handler()

        self.__new_game.display(self.__screen, 0,0)
        self.__continue.display(self.__screen, 0,0)

        return continue_looping

    def __event_handler(self):
        """
        Method for handling events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True



if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    level = CStart(CSceneManager())
    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = level.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
