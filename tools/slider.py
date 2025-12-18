"""
Tools for working with sliders 
"""
import pygame
from tools.utils import percetage

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

        self.__stop     = (0,0)
        self.__speed    = 0

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

    def __assign_stop(self, stop : str) -> tuple:
        """
        Assigns stops
        """
        size = self.__screen.get_rect().size
        stops = {
            "TABLE": (0,0),
            "CANVAS" : (0, -size[1] + percetage(size[1], 5)),
            "END" : (0, -size[1]*2 + percetage(size[1], 5)),
            "ATTEMPTS": (-size[0] + percetage(size[0], 5),0), 
            "INVENTAR" : (size[0] - percetage(size[0], 5),0)
        }
        return stops[stop]

    def move_to(self, where : str, speed : int):
        """
        Sets destination where to move
        """
        self.__stop = self.__assign_stop(where)
        self.__speed = speed
        print(self.__stop, " , ", self.__speed)

    def arrived(self, global_x, global_y) -> bool:
        """
        Checks if slider moved scene to right position
        """
        buff = [False, False]
        if self.__speed < 0:
            print("here < ")
            if  (   self.__stop[0]  +self.__speed  <= global_x and
                    self.__stop[0] -self.__speed  >= global_x
                ):
                buff[0] = True
            if  (   self.__stop[1]  +self.__speed <= global_y and
                    self.__stop[1] -self.__speed  >= global_y
                ):
                buff[1] = True
        elif self.__speed > 0:
            print("here >")
            if  (   self.__stop[0]  +self.__speed >= global_x and
                    self.__stop[0] -self.__speed  <= global_x
                ):
                buff[0] = True
            if  (   self.__stop[1]  +self.__speed >= global_y and
                    self.__stop[1] -self.__speed  <= global_y
                ):
                buff[1] = True
        if buff[0] and buff[1]:
            self.__speed = 0
        return buff[0] and buff[1]

    def center(self):
        """
        Call after scene moved to center 
        """
        return self.__stop



if __name__ == "__main__":
    ...
