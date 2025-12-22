"""
Script that generates menu
"""
import pygame
from tools.anim_button import CAnimButton, CAnimations

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

#WIZ_IDLE  500x500
#WIZ_HOVER 500x500


class CMenu:
    """
    Class for handling menu
    """
    def __init__(self):
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__wizzad = CAnimButton(pos = (SCREEN_W , SCREEN_H),
                                    idle = CAnimations("assets/wiz_idle", fps = 5),
                                    hovered= CAnimations("assets/wiz_hover", fps = 5),
                                    pressed= CAnimations("assets/wiz_pres", fps=5),
                                    on_press = self.start_shoping,
                                    on_release= self.exit_shoping)

        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

    def display_menu(self, delta_time):
        """
        Method for displaying menu,
        intended to be called in 
        main game_loop 
        """
        self.__screen.fill((0,0,0))
        continue_looping = self.handle_events()
        self.__wizzad.display(self.__screen, 0, 0, delta_time)

        return continue_looping

    def handle_events(self) -> bool:
        """
        Method for handling events 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def start_shoping(self):
        """
        Metod for shoping with wizzard
        """
        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

    def exit_shoping(self):
        """
        Metod for extting shop with wizzard
        """
        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))


if __name__ == "__main__":
    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    clock = pygame.time.Clock()

    menu = CMenu()

    while RUNNING:

        RUNNING = menu.display_menu(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
