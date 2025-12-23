"""
Script that generates menu
"""
import pygame
from tools.anim_button import CAnimButton, CAnimations
from tools.button      import CButton

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

        temp_pos = (0,0)
        self.__easy     = CButton(  position = temp_pos,
                                    idle = "assets/difficultie_posters/EASY_idle.png")
        self.__medium   = CButton(  position = temp_pos,
                                    idle = "assets/difficultie_posters/MEDIUM_idle.png")
        self.__hard   = CButton(    position = temp_pos,
                                    idle = "assets/difficultie_posters/HARD_idle.png")

        self.__wizzad = CAnimButton(pos = (SCREEN_W , SCREEN_H),
                                    idle = CAnimations("assets/wiz_idle", fps = 5),
                                    hovered= CAnimations("assets/wiz_hover", fps = 5),
                                    pressed= CAnimations("assets/wiz_pres", fps=5),
                                    on_press = self.start_shoping,
                                    on_release= self.exit_shoping)

        self.__easy.move((250, SCREEN_H - 1.5 * self.__easy.height()))
        self.__medium.move((450, SCREEN_H - 2 * self.__medium.height()))

        temp_pos = self.__center_align(self.__hard.get_idle())
        self.__hard.move((temp_pos[0], 100))

        self.__board = pygame.image.load("assets/bounty_board.png")

        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

    def display_menu(self, delta_time):
        """
        Method for displaying menu,
        intended to be called in 
        main game_loop 
        """
        self.__screen.fill((0,0,0))
        continue_looping = self.handle_events()

        self.__screen.blit(self.__board, self.__center_align(self.__board))

        self.__easy.display(self.__screen, 0, 0)
        self.__medium.display(self.__screen, 0, 0)
        self.__hard.display(self.__screen, 0, 0)

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

    def __center_align(self, surf : pygame.Surface):
        """
        find center cordinates for given surf
        """
        size = surf.get_rect().size
        pos = (SCREEN_W // 2 - size[0]//2, SCREEN_H // 2 - size[1]//2)
        return pos


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
