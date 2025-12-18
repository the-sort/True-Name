"""
Button Module
"""
import pygame

class CButton:
    """
    Class for working and displaying buttons
    """
    def __init__(self,  idle            ,
                        position        ,
                        width      = 0  ,
                        height     = 0  ,
                        hovered    = "" ,
                        pressed    = ""
                ):
        """
        position argmuent is tuple of topleft corner
        """
        self.__idle_img        = self.__load_image(idle, width, height)
        self.__hovered_img     = self.__load_image(hovered, width, height)
        self.__pressed_img     = self.__load_image(pressed, width, height)

        self.__position = position


    def display (self,  screen : pygame.Surface, 
                        event : pygame.Event,
                        global_x,
                        global_y
                ):
        """
        Metod for displaying button in scene
        """
        pos = (self.__position[0] + global_x, self.__position[1] + global_y)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.__pressed(event.pos):
            screen.blit(self.__pressed_img, pos)
            return
        if event.type == pygame.MOUSEMOTION and self.__hovered(event.pos):
            screen.blit(self.__hovered_img, pos)
            return
        screen.blit(self.__idle_img, pos)



    def __load_image(self, path, width, height):
        """
        Metod for loading optional
        button states
        """
        if path == "":
            return None
        img = pygame.image.load(path)
        return self.__transform(img, width, height)

    def __hovered(self, pos : tuple) -> bool:
        """
        Checks if player hovers over button
        """
        if self.__hovered_img is None:
            return False
        return self.__hovered_img.get_rect().collidepoint(pos)

    def __pressed(self, pos : tuple) -> bool:
        """
        Checks if player pressed button
        """
        if self.__pressed_img is None:
            return False
        return self.__pressed_img.get_rect().collidepoint(pos)

    def __transform(self, img : pygame.Surface, width, height):
        """
        Transform button to desired scale
        """
        if width == 0:
            width = img.get_rect().width
        if height == 0:
            height = img.get_rect().height
        return pygame.transform.scale(img, (width, height))



if __name__ == "__main__":
    ...
