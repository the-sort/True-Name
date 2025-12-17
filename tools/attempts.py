"""
This module displays
all users answers and their likness 
on right side of level
"""
import pygame



class CAttempts:
    """
    Class for handling and displaying users answers
    """
    def __init__(self, screen):
        self.__attempts = []
        self.__screen   = screen
        self.__screen_width = self.__screen.get_width()

    def add(self, attempt : tuple):
        """
        Adds users attempt
        param:  attempt[0] str
                attempt[1] int
        """
        self.__attempts.append(attempt)

    def display_attempts(self, global_x, global_y):
        """
        Display users attempts
        Expected to be called in game_loop
        """
        font_size = 25
        color   = (255, 255, 255)
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
        x_off = font_size + 10
        y_off = font_size
        for attempt in self.__attempts:
            text = str(attempt[0])
            text_surface = font.render(text, True, color)

            self.__screen.blit  (text_surface, (x_off + global_x + self.__screen_width,
                                                y_off + global_y)
                                )
            text = "LIKNESS  =  " + str(attempt[1])
            text_surface = font.render(text, True, color)
            self.__screen.blit  (text_surface, ((2 * self.__screen_width - (text_surface.get_width() + 2.5*font_size)) + global_x,
                                                y_off + global_y))
            y_off += font_size + font.get_height()

if __name__ == "__main__":
    ...
