"""
Script creates level 
"""
import pygame
import tools.table_generator as tg
import tools.brush as brush
import tools.canvas as canvas
import tools.attempts as attempts
from tools.slider import CSlider as Slider, SLIDER_H
from tools.evaluator import CEvaluator
from tools.utils import  CDificulties
from tools.button import CButton

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

class CLevel:
    """
    Metods for handling level
    """
    def __init__(self, manager, difficultie : str, language = "ENG"):
        self.__manager = manager

        self.__difficultie = CDificulties(difficultie)

        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__table  = tg.CTable(self.__screen, self.__difficultie, language)
        self.__attempts = attempts.CAttempts(self.__screen)

        self.__x_pos    = 0
        self.__y_pos    = 0
        self.__x_off    = 0
        self.__y_off    = 0

        self.__canvases = canvas.CCanvases(SCREEN_H)
        self.__brush = brush.CBrush()
        self.__evaluator = CEvaluator()

        self.__center_collider = Slider(    screen  = self.__screen                           ,
                                            left    = SCREEN_W // 2                ,
                                            top     = SCREEN_H - SLIDER_H       ,
                                            rotation = 180 ,
                                            active  = True,
                                            center_x= True,
                                            center_y= False
                                        )
        self.__right_collider = Slider (    screen  = self.__screen                     ,
                                            left    = SCREEN_W - SLIDER_H ,
                                            top     = SCREEN_H // 2 - 20                                  ,
                                            scale_x = 1            ,
                                            scale_y = 1                         ,
                                            rotation= -90,
                                            center_x= False,
                                            center_y= True
                                        )
        self.__end_slider     = Slider  (   screen  = self.__screen                               ,
                                            left    = SCREEN_W // 2                     ,
                                            top     = (SCREEN_H * 2) - 2*SLIDER_H,
                                            scale_x = 1    ,
                                            scale_y =  1                 ,
                                            rotation= 180,
                                            active  = False,
                                            center_x = True,
                                            center_y= False
                                        )
        self.__deactivated_sliders = False

        self.__exit = CButton   (   idle = "assets/exit/exit_door_idle.png",
                                    hovered="assets/exit/exit_door_hovered.png",
                                    position = (SCREEN_W // 2, SCREEN_H * 3 - SCREEN_H//2 - 1.4*SLIDER_H),
                                    width =  77*6.5,
                                    height = 99*6.5
                                )
        self.__exit.center()
    def display(self, delta_time):
        """
        Metod called in game loop
        """

        self.__screen.fill((0,0,0))
        self.__table.display_table(self.__x_pos, self.__y_pos)


        self.__center_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__right_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__end_slider.display_slider(self.__x_pos, self.__y_pos)

        continue_looping = self.__event_handler(self.__x_pos, self.__y_pos, delta_time)

        self.__exit.display(self.__screen, self.__x_pos, self.__y_pos)

        self.__canvases.display_canvases(self.__screen, self.__x_pos, self.__y_pos)
        self.__attempts.display_attempts(self.__x_pos, self.__y_pos)

        self.__evaluator.guess(self.__screen, self.__x_pos, self.__y_pos)

        self.__manager.player.display_health(self.__screen, self.__x_pos, self.__y_pos)

        if  (   (buff := self.__center_collider.arrived(self.__x_pos, self.__y_pos)) or
                self.__end_slider.arrived(self.__x_pos, self.__y_pos)
            ):
            self.__x_pos, self.__y_pos = self.__center_collider.center() if  buff else self.__end_slider.center()
            self.__y_off = 0
            self.__activate_sliders()

        if  self.__right_collider.arrived(self.__x_pos, self.__y_pos):
            self.__x_pos, self.__y_pos = self.__right_collider.center()
            self.__x_off = 0
            self.__activate_sliders()

        self.__x_pos += self.__x_off
        self.__y_pos += self.__y_off
        return continue_looping

    def __event_handler(self, global_x, global_y, delta_time):
        """
        Metod handling all inputs and events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False #END GAME
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    if self.__exit.is_pressed(event.pos, (self.__x_pos, self.__y_pos)):
                        self.__manager.player.add_coins(self.__difficultie.reward())
                        self.__manager.player.save()
                        while pygame.mouse.get_pressed()[0]:
                            pygame.event.get()
                        self.__manager.change_scene(self.__manager, "MENU")
                    self.__brush.down()
                    if  (   self.__end_slider.is_active() and
                            self.__end_slider.collidepoint(global_x, global_y, event.pos)
                        ):
                        if self.__y_pos <= -SCREEN_H * 2 + 2 * SLIDER_H:
                            self.__end_slider.move_to("CANVAS", 8)
                            self.__y_off = 8
                        else :
                            self.__end_slider.move_to("END", -8)
                            self.__y_off = -8
                if not self.__deactivated_sliders:
                    if self.__center_collider.collidepoint(global_x, global_y, event.pos):
                        if self.__y_pos >= 0:
                            self.__y_off = -8
                            self.__center_collider.move_to("CANVAS", -8)
                        else:
                            self.__y_off = 8
                            self.__center_collider.move_to("TABLE", 8)
                        self.__deactivate_sliders()
                    elif self.__right_collider.collidepoint(global_x, global_y, event.pos):
                        if self.__x_pos >= 0:
                            self.__x_off = -8
                            self.__right_collider.move_to("ATTEMPTS", -8)
                        else:
                            self.__x_off = 8
                            self.__right_collider.move_to("TABLE", 8)
                        self.__deactivate_sliders()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   # left click
                    self.__brush.up()
                    self.__evaluator.changed()
                if event.button == 3:
                    self.__canvases.make_blank(event.pos)
                    self.__evaluator.changed()
            if event.type == pygame.MOUSEMOTION and self.__brush.is_down():
                if (a_canvas := self.__canvases.get_active(event.pos)) is None:
                    continue
                self.__brush.draw(a_canvas[0], a_canvas[1], event.pos)

                self.__manager.player.deacrease_health(self.__difficultie.health_drain() * delta_time)
                self.__manager.player.display_dripping( self.__screen,
                                                        delta_time,
                                                        self.__x_pos,
                                                        self.__y_pos
                                                      ) #deffinietly not 30FPS but looks dope
                if self.__manager.player.health() <= 0:
                    break
                pygame.image.save   (   a_canvas[0],
                                        f"profile/input/char{a_canvas[2]}.png"
                                    ) #Preanswer guessing
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__canvases.save()
                answer = self.__evaluator.make_string(True) #Finall Answer guessing
                if (likness := self.__table.check_solution(answer))[0]:
                    self.__end_slider.activate()
                else:
                    self.__canvases = canvas.CCanvases(SCREEN_H)
                    self.__attempts.add((answer, likness[1]))

        if self.__manager.player.health() <= 0:
            while pygame.mouse.get_pressed()[0]:
                pygame.event.get()
            self.__manager.change_scene(self.__manager, "MENU")

        return True

    def __deactivate_sliders(self):
        """
        Deactivates all sliders
        """
        self.__deactivated_sliders = True

    def __activate_sliders(self):
        """
        activates all sliders
        """
        self.__deactivated_sliders = False
    def __del__(self):
        self.__manager.player.heal_to_full()

if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    level = CLevel(CSceneManager(),"MEDIUM")
    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = level.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
