"""
Scene for displaying wheter player
completed level or not
"""
import pygame
from tools.button import CButton
from tools.utils import CDificulties

SCREEN_W = 500
SCREEN_H = 500

class CSummary:
    """
    Class for displaying and handling
    post level summary
    """
    def __init__(self, manager, completed, difficultie):
        self.__manager = manager

        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

        button_size = (350, 150)
        off_set = 10

        continue_pos = (SCREEN_W//2 - button_size[0]//2, SCREEN_H - button_size[1])
        self.__continue = CButton(
            position = continue_pos,
            idle = "assets/summary/continue_scaled.png",
            on_press = self.go_to_menu
        )

        retry_pos = (SCREEN_W//2 - button_size[0]//2, SCREEN_H - 2*button_size[1] - off_set)
        self.__retry = CButton(
            position = retry_pos,
            idle = "assets/summary/retry.png",
            on_press = lambda : self.restart_level(difficultie),
            visible = False if completed else True,
            active = False if completed else True
        )

        self.__coin_img = pygame.image.load("assets/coin_scaled.png")

        self.__header = self.__create_header(completed)
        self.__header_size = self.__header.get_rect().size

        self.__sub_header = self.__create_sub_header(difficultie, completed)
        self.__sub_header_size = self.__sub_header.get_rect().size


    def display(self, _delta_time):
        """
        Metod for displaying class in
        game loop
        """
        off_set = 10

        self.__screen.fill((0, 0, 0))

        self.__screen.blit(self.__header, (SCREEN_W//2 - self.__header_size[0]//2, 0))
        self.__screen.blit(self.__sub_header, (0, self.__header_size[1] + off_set))

        coin_img_pos = (self.__sub_header_size[0] + off_set, self.__header_size[1] + off_set)
        self.__screen.blit(self.__coin_img, coin_img_pos)

        self.__continue.display(self.__screen, 0, 0)
        self.__retry.display(self.__screen, 0, 0)

        continue_looping = self.__event_handler()

        return continue_looping

    def go_to_menu(self):
        """
        Metod for continue button
        to send Player to menu
        """
        while pygame.mouse.get_pressed()[0]:
            pygame.event.get()
        self.__manager.change_scene(self.__manager, "MENU")
        return "MENU"

    def restart_level(self, difficultie):
        """
        Metod for retry button
        to restart level
        """
        while pygame.mouse.get_pressed()[0]:
            pygame.event.get()
        self.__manager.change_scene(self.__manager, difficultie)
        return difficultie


    def __event_handler(self) -> bool:
        """
        Metod for handling events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def __create_header(self, completed, color=(255, 255, 255)):
        """
        Metod for prerendering header text
        """

        font_size = 35
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)

        if completed:
            text = "Level Complete"

        else:
            text = "Game Over"

        return font.render(text, True, color)

    def __create_sub_header(self, difficultie, completed, color = (255, 255, 255)):
        """
        Metod for prerendering 
        sub header text
        """
        font_size = 25
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
        difficultie = CDificulties(difficultie)

        reward = str(difficultie.reward()) if completed else "0"

        text = f"REWARD:    {reward}"
        return font.render(text, True, color)


if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING = True
    DELTA_TIME = 0.1

    pygame.init()
    t_manager = CSceneManager()
    t_manager.change_scene(t_manager, "LOOSE", "HARD")

    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = t_manager.scene.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
