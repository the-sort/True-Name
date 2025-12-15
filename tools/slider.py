"""
Tools for working with sliders 
"""
import pygame

class CSlider:
    """
    Slider
    """
    def __init__(self,screen, left, top, width, height, active = True):
        self.__screen = screen

        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

        self.__active   = active
        self.__slider   = pygame.Rect   (  self.__left,
                                           self.__top ,
                                           self.__width,
                                           self.__height
                                        )

    def is_active(self) -> bool:
        """
        Checks if slider should be displayed
        """
        return self.__active

    def activate(self):
        """
        Activate slider
        """
        self.__active = True

    def deactivate(self):
        """
        Deactivate slider
        """
        self.__active = False

    def display_slider(self, global_x, global_y):
        """
        Display slider into scene
        """
        if not self.__active:
            return
        self.__slider = pygame.Rect   (    self.__left + global_x,
                                           self.__top  + global_y,
                                           self.__width,
                                           self.__height
                                        )
        color = (255, 255, 255)
        pygame.draw.rect(self.__screen, color, self.__slider)

    def collidepoint(self, global_x, global_y, pos) -> bool:
        """
        Checks for colision using position
        """
        self.__slider.move((global_x, global_y))
        return self.__slider.collidepoint(pos)


if __name__ == "__main__":
    ...
