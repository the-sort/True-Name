"""
Button Module
"""
import pygame

class CButton:
    """
    Class for working and displaying buttons
    """
    def __init__(self,  position            ,
                        idle                ,
                        action       = None ,
                        width        = 0    ,
                        height       = 0    ,
                        hovered      = ""   ,
                        pressed      = ""
                ):
        """
        position argmuent is tuple of topleft corner
        """
        self.__idle_img        = self.__load_image(idle, width, height)
        self.__hovered_img     = self.__load_image(hovered, width, height)
        self.__pressed_img     = self.__load_image(pressed, width, height)

        self.__action = action

        self.__state = False

        self.__was_pressed = False

        self.__position = position


    def display (self,  screen : pygame.Surface,
                        global_x,
                        global_y,
                        delta_time = None
                ):
        """
        Metod for displaying button in scene
        """
        global_pos = (self.__position[0] + global_x, self.__position[1] + global_y)
        mouse_pos   = pygame.mouse.get_pos()

        pressed = self.is_pressed(mouse_pos, (global_x, global_y))

        if delta_time is not None:
            raise ValueError("Invalid value delta_time passed")

        self.__released(pressed)

        # if pressed:
        #     self.__call()

        if self.__state and self.__pressed_img is not None:
            screen.blit(self.__pressed_img, global_pos)
            return

        if self.__hovered(mouse_pos, global_pos):
            screen.blit(self.__hovered_img, global_pos)
            return

        screen.blit(self.__idle_img, global_pos)

    def center(self):
        """
        Centers Image according to
        possition cordinates
        """
        img_size = self.__idle_img.get_rect().size
        self.__position =   (self.__position[0] - img_size[0] // 2,
                             self.__position[1] - img_size[1] // 2
                            )

    def is_pressed(self, mouse_pos : tuple, global_off : tuple) -> bool:
        """
        Checks wheter button was pressed
        """
        pos = (self.__position[0] + global_off[0], self.__position[1] + global_off[1])
        l_click     = pygame.mouse.get_pressed()[0]
        return self.__idle_img.get_rect(topleft = pos).collidepoint(mouse_pos) and l_click


    def __load_image(self, path, width, height):
        """
        Metod for loading optional
        button states
        """
        if path == "":
            return None
        if isinstance(path, pygame.Surface):
            return path
        img = pygame.image.load(path)
        return self.__transform(img, width, height)

    def __hovered(self, mouse_pos : tuple, global_pos : tuple) -> bool:
        """
        Checks if player hovers over button
        """
        if self.__hovered_img is None:
            return False
        return self.__hovered_img.get_rect(topleft = global_pos).collidepoint(mouse_pos)

    def __released(self, pressed):
        """
        Set state to 0
        """
        if pressed != self.__was_pressed and pressed:
            self.__state = not self.__state
            self.__call()
        self.__was_pressed = pressed


    def __transform(self, img : pygame.Surface, width, height):
        """
        Transform button to desired scale
        """
        if width == 0:
            width = img.get_rect().width
        if height == 0:
            height = img.get_rect().height
        return pygame.transform.scale(img, (width, height))

    def __call(self):
        """
        Calls action
        """
        if self.__action is not None and self.__state:
            self.__action()

    def right_bottom(self, screen_size):
        """
        Moves button to the
        right bottom corner
        """
        size = self.__idle_img.get_rect().size
        self.__position = (screen_size[0] - size[0], screen_size[1] - size[1])



if __name__ == "__main__":
    ...
