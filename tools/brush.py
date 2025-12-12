"""
Handling users drawings
"""
import pygame

class CBrush:
    """
    class that represents brush
    """
    def __init__(self, color = (255, 0, 0), size = 4):
        self.__down  = False
        self.__color = color
        self.__size  = size

    def up(self):
        """
        Lift brush from canvas
        """
        self.__down  = False

    def down(self):
        """
        Place brush on canvas
        """
        self.__down = True

    def is_down(self) -> bool:
        """
        Checks if brush is on canvas
        """
        return self.__down

    def draw(self, canvas, canvas_rect, pos):
        """
        Puts a pixel on canvas
        """
        pixel = pygame.Rect (   pos[0] - canvas_rect.x  ,
                                pos[1] - canvas_rect.y  ,
                                self.__size             ,
                                self.__size
                            )
        pygame.draw.rect(canvas, self.__color, pixel)
