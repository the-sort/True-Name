"""
helper functions
"""
import PIL


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
