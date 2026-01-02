"""
helper functions
"""
import PIL

class CDificulties:
    """
    Class for handling difficulties
    """
    def __init__(self, difficultie):
        self.__set_difficultie(difficultie)

    def cols(self):
        """
        Returns am of cols
        """
        return  self.__cols

    def rows(self):
        """
        Returns am of rows
        """
        return  self.__rows

    def scale(self):
        """
        Returns am of table window scale
        """
        return  self.__scale

    def font_size(self):
        """
        Returns am of table font size
        """
        return self.__font_size

    def health_drain(self):
        """
        Returns health drain when writing
        """
        return self.__health_drain

    def reward(self):
        """
        Returns reward for completing level
        """
        return self.__reward

    def difficultie(self) -> str:
        """
        Returns set difficultie
        """
        return self.__difficultie

    def __set_difficultie(self, difficultie):
        """
        Sets difficultie of table
        """
        match difficultie:
            case "EASY":
                self.__difficultie  = "EASY"
                self.__cols         = 6
                self.__rows         = 5
                self.__scale        = 5
                self.__font_size    = 35
                self.__health_drain = -0.25
                self.__reward       = 50
                return
            case "MEDIUM":
                self.__difficultie  = "MEDIUM"
                self.__cols         = 8
                self.__rows         = 6
                self.__scale        = 4
                self.__font_size    = 30
                self.__health_drain = -0.5
                self.__reward       = 100
                return
            case "HARD":
                self.__difficultie  = "HARD"
                self.__cols         = 16
                self.__rows         = 12
                self.__scale        = 2
                self.__font_size    = 15
                self.__health_drain = -1
                self.__reward       = 200
                return



def percetage(number, percent) -> int:
    """
    calculates given percetange of given number
    """
    return number * percent / 100

def is_blank(image, background = (255, 255, 255)) -> bool:
    """
    Checks if given image is blank
    """
    colors = image.getcolors()
    return len(colors) == 1 and colors[0][1] == background
