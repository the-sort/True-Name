"""
Module for button 
with animations
"""
import pygame
from tools.animator import CAnimations
from tools.button   import CButton


class CAnimButton(CButton):
    """
    Button with animations
    """
    def __init__(   self,
                    pos                         ,
                    idle    : CAnimations       ,
                    action               = None ,
                    hovered : CAnimations = None,
                    pressed : CAnimations = None
                ):

        super().__init__(pos, idle = idle.get_keyframe(), action= action)

        self.__idle_anim    =  idle
        self.__hovered_anim = hovered
        self.__pressed_anim = pressed

    def display(self,   screen : pygame.Surface,
                        global_x,
                        global_y,
                        delta_time = None
                ):
        """
        Displays animation to the scene
        """
        global_pos = (self._CButton__position[0] + global_x, self._CButton__position[1] + global_y)
        mouse_pos  = pygame.mouse.get_pos()
        l_click    = pygame.mouse.get_pressed()[0]

        if l_click and self._CButton__pressed(mouse_pos, global_pos):
            self.__pressed_anim.play(screen, delta_time, global_pos)
            return

        if self.is_pressed(mouse_pos, (global_x, global_y)):
            self._CButton__call()
        else:
            self._CButton__released()
        if l_click and self._CButton__hovered(mouse_pos, global_pos):
            self.__hovered_anim.play(screen, delta_time, global_pos)
            return
        self.__idle_anim.play(screen, delta_time, global_pos)


if __name__ == "__main__":
    buff = pygame.display.set_mode((100,100))
    test = CAnimButton((0,0), CAnimations("assets/wiz_idle"))
    test.display(buff, 10, 10, 0.0001)
