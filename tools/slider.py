"""
Tools for working with sliders 
"""
import pygame

SLIDER_W   = 600
SLIDER_H   = 100

class CSlider:
    """
    Slider
    """
    def __init__(self,  screen          ,
                        left            ,
                        top             ,
                        scale_x = 1     ,
                        scale_y = 1     ,
                        rotation = 0    ,
                        active = True   ,
                        center_x = True ,
                        center_y = True
                ):
        self.__screen = screen

        self.__left = left
        self.__top  = top

        self.__stop     = (0,0)
        self.__speed    = 0

        self.__active   = active

        self.__slider = self.__preprocess_img(scale_x, scale_y, rotation) #slider.png (600x100) by default

        if center_x:
            self.__center_x()
        if center_y:
            self.__center_y()


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

    def display_slider  (self, global_x, global_y):
        """
        Display slider into scene
        """
        if not self.__active:
            return

        global_pos = (self.__left + global_x, self.__top + global_y)
        self.__screen.blit(self.__slider, global_pos)

    def collidepoint(self, global_x, global_y, pos) -> bool:
        """
        Checks for colision using position
        """
        topleft = (self.__left + global_x, self.__top + global_y)
        rect = self.__slider.get_rect(topleft = topleft)
        return rect.collidepoint(pos)

    def __assign_stop(self, stop : str) -> tuple:
        """
        Assigns stops
        """
        size = self.__screen.get_rect().size
        stops = {
            "TABLE": (0,0),
            "CANVAS" : (0, -size[1] + SLIDER_H),
            "END" : (0, -size[1]*2 + SLIDER_H),
            "ATTEMPTS": (-size[0] + SLIDER_H,0), 
            "INVENTAR" : (size[0] - SLIDER_H,0)
        }
        return stops[stop]

    def move_to(self, where : str, speed : int):
        """
        Sets destination where to move
        """
        self.__stop = self.__assign_stop(where)
        self.__speed = speed

    def arrived(self, global_x, global_y)-> bool:
        """
        Checks if slider moved scene to right position
        """
        buff = [False, False]
        if self.__speed < 0:
            if  (   self.__stop[0]  +self.__speed  <= global_x and
                    self.__stop[0] -self.__speed  >= global_x
                ):
                buff[0] = True
            if  (   self.__stop[1]  +self.__speed <= global_y and
                    self.__stop[1] -self.__speed  >= global_y
                ):
                buff[1] = True
        elif self.__speed > 0:
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

    def __preprocess_img(self, scale_x, scale_y, rotation):
        """
        Metod used for img preprocesing
        """
        img = pygame.image.load("assets/slider/slider.png")

        width  = img.get_width()  * scale_x
        height = img.get_height() * scale_y

        img = pygame.transform.scale(img, (width, height))
        img = pygame.transform.rotate(img, rotation)
        return img

    def __center_x(self):
        """
        Centers slider in x_axis
        """
        width = self.__slider.get_width()
        self.__left -= width // 2

    def __center_y(self):
        """
        Centers slider in y_axis
        """
        height = self.__slider.get_height()
        self.__top -= height // 2




if __name__ == "__main__":
    ...
