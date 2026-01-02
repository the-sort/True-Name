"""
This module displays
all users answers and their likness 
on right side of level
"""
import pygame
from tools.slider import SLIDER_H



class CAttempts:
    """
    Class for handling and displaying users answers
    """
    def __init__(self, screen):
        self.__attempts = [""] * 11
        self.__amount = 0
        self.__screen   = screen
        self.__screen_width = self.__screen.get_width()

    def add(self, attempt : tuple):
        """
        Adds users attempt
        param:  attempt[0] str
                attempt[1] int
        11 fits into screen
        """
        self.__amount %= 11
        self.__attempts[self.__amount] = attempt
        self.__amount += 1


    def display_attempts(self, global_x, global_y):
        """
        Display users attempts
        Expected to be called in game_loop
        """
        font_size = 20
        color   = (255, 255, 255)
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
        x_off = SLIDER_H + font_size
        y_off = font_size
        for attempt in self.__attempts:
            if attempt == "":
                continue

            text = str(attempt[0])
            text_surface = font.render(text, True, color)
            self.__screen.blit  (
                                    text_surface,
                                    (
                                        x_off + global_x + self.__screen_width - SLIDER_H,
                                                y_off + global_y
                                    )
                                )

            text = "LIKNESS  =  " + str(attempt[1])
            text_surface = font.render(text, True, color)
            text_pos =  (
                            (
                                2 * self.__screen_width
                                -
                                (text_surface.get_width() + font_size + SLIDER_H)
                            ) + global_x,
                            y_off + global_y
                        )
            self.__screen.blit  (text_surface, text_pos)
            y_off += font_size + font.get_height()

if __name__ == "__main__":
    ...
