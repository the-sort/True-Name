"""
Tool for displaying and handling canvas
"""
import pygame
import numpy as np

class CCanvases:
    """
    Class for handling drawing canvas
    """
    def __init__(self, screen_height):
        self.__screen_height = screen_height

        self.__width            = 175
        self.__height           = 175
        self.__canvases         = [pygame.Surface((self.__width,self.__height)) for _ in range(10)]
        self.__canvases_rect    = [canvas.get_rect() for canvas in self.__canvases]

        self.__frame = pygame.image.load("frame.png")

        self.__background = (255,255,255)

        for canvas in self.__canvases:
            canvas.fill(self.__background)


    def display_canvases(self, screen, global_x, global_y):
        """
        Metod used for displaying canvases
        """
        x_offset = 74
        for i in range(5):
            l_corner =  (
                        x_offset + global_x,
                        (self.__screen_height//2) + self.__screen_height + global_y - self.__height
                        )

            screen.blit(self.__canvases[i], l_corner)
            screen.blit(self.__frame, l_corner)
            self.__canvases_rect[i] = self.__canvases[i].get_rect(topleft = l_corner)
            x_offset += 175

        x_offset = 74
        for i in range(5,10):
            l_corner =  (
                        x_offset + global_x,
                        (self.__screen_height//2) + self.__screen_height + global_y
                        )
            screen.blit(self.__canvases[i], l_corner)
            screen.blit(self.__frame, l_corner)
            self.__canvases_rect[i] = self.__canvases[i].get_rect(topleft = l_corner)
            x_offset += 175
    def get_active(self, pos):
        """
        Metod that returns canvas with 
        which player interacts
        Return None if interacts with nothing
        Return Surface, rect and index when found
        """
        for i in enumerate(self.__canvases):
            if self.__canvases_rect[i[0]].collidepoint(pos):
                return (i[1], self.__canvases_rect[i[0]], i[0])
        return None

    def save(self):
        """
        Saves users answer
        """
        x = 0
        for canvas in self.__canvases:
            pygame.image.save(canvas, "profile/input/char" + str(x) + ".png")
            x += 1
        print("SAVING CANVAS")


    def is_blank(self, canvas):
        """
        Controls if canvas is blank
        """
        return np.all(pygame.surfarray.array3d(canvas) == self.__background)
