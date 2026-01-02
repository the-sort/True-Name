"""
Scene for displaying wheter player
completed level or not
"""
import pygame
from tools.button import CButton

SCREEN_W = 500
SCREEN_H = 500

class CSummary:
    """
    Class for displaying and handling
    post level summary
    """
    def __init__(self, manager, completed):
        self.__manager = manager

        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

        button_size = (250, 150)

        self.__continue = CButton   (   position     = (SCREEN_W // 2 - button_size[0] // 2, SCREEN_H - button_size[1]),
                                        idle         = "assets/continue_scaled.png",
                                        on_press = self.go_to_menu
                                    )

        self.__header = self.__create_header(completed)
        self.__header_size = self.__header.get_rect().size


    def display(self, _delta_time):
        """
        Metod for displaying class in
        game loop
        """
        self.__screen.fill((0, 0, 0))

        self.__screen.blit(self.__header, (SCREEN_W // 2 - self.__header_size[0] // 2, 0))
        self.__continue.display(self.__screen, 0, 0)

        continue_looping = self.__event_handler()

        return continue_looping

    def go_to_menu(self):
        """
        Metod for continue button
        to send Player to menu
        """
        self.__manager.change_scene(self.__manager, "MENU")


    def __event_handler(self) -> bool:
        """
        Metod for handling events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def __create_header(self, completed, color = (255, 255, 255)):
        font_size = 35
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)

        if completed:
            text = "Level Complete"
        else:
            text = "Game Over"
        return font.render(text, True, color)



if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    t_manager = CSceneManager()
    t_manager.change_scene(t_manager, "LOOSE")

    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = t_manager.scene.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
