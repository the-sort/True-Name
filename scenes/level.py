"""
Script creates level 
"""
import pygame
from tools.utils import percetage
import tools.table_generator as tg
import tools.brush as brush
import tools.canvas as canvas
import tools.attempts as attempts
from tools.slider import CSlider as Slider
from tools.evaluator import CEvaluator
from tools.player import CPlayer
from tools.utils import  CDificulties

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

class CLevel:
    """
    Metods for handling level
    """
    def __init__(self, difficultie : str, language = "ENG"):
        self.__difficultie = CDificulties(difficultie)

        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__table  = tg.CTable(self.__screen, self.__difficultie, language)
        self.__attempts = attempts.CAttempts(self.__screen)
        self.__player  = CPlayer()

        self.__x_pos    = 0
        self.__y_pos    = 0
        self.__x_off    = 0
        self.__y_off    = 0

        self.__canvases = canvas.CCanvases(SCREEN_H)
        self.__brush = brush.CBrush()
        self.__evaluator = CEvaluator()

        self.__center_collider = Slider(    self.__screen, percetage(SCREEN_W, 10)  ,
                                            SCREEN_H - percetage(SCREEN_H, 5)       ,
                                            SCREEN_W - 2 * percetage(SCREEN_W, 10)  ,
                                            percetage(SCREEN_H, 5)                  ,
                                            active = True
                                        )
        self.__left_collider = Slider  (    self.__screen,   0      ,
                                            0                       ,
                                            percetage(SCREEN_W, 5)  ,
                                            SCREEN_H                ,
                                            active = True
                                        )
        self.__right_collider = Slider (    self.__screen,  SCREEN_W - percetage(SCREEN_W, 5) ,
                                            0                                                 ,
                                            percetage(SCREEN_W, 5)                            ,
                                            SCREEN_H                                          ,
                                            active = True
                                        )
        self.__end_slider     = Slider  (   self.__screen, percetage(SCREEN_W, 10)      ,
                                            (SCREEN_H * 2) - percetage(2 * SCREEN_H, 5) ,
                                            SCREEN_W - 2 * percetage(SCREEN_W, 10)      ,
                                            percetage(2 * SCREEN_H, 5)                  ,
                                            active = True
                                        )
    def display_level(self, delta_time):
        """
        Metod called in game loop
        """

        self.__screen.fill((0,0,0))
        self.__table.display_table(self.__x_pos, self.__y_pos)

        self.__center_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__left_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__right_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__end_slider.display_slider(self.__x_pos, self.__y_pos)

        continue_looping = self.__event_handler(self.__x_pos, self.__y_pos, delta_time)

        self.__canvases.display_canvases(self.__screen, self.__x_pos, self.__y_pos)
        self.__attempts.display_attempts(self.__x_pos, self.__y_pos)

        self.__evaluator.guess(self.__screen, self.__x_pos, self.__y_pos)

        self.__player.display_health(self.__screen, self.__x_pos, self.__y_pos)


        # print(self.__y_pos)
        # if  self.__y_pos <= -SCREEN_H + percetage(SCREEN_H, 5) or self.__y_pos >= 0:
        #     self.__y_off = 0
        if  (buff := self.__center_collider.arrived(self.__x_pos, self.__y_pos)) or self.__end_slider.arrived(self.__x_pos, self.__y_pos): #or self.__end_slider.arrived(self.__x_pos, self.__y_pos)
            self.__x_pos, self.__y_pos = self.__center_collider.center() if  buff else self.__end_slider.center()
            self.__y_off = 0


        
        if  (  (buff :=self.__left_collider.arrived(self.__x_pos, self.__y_pos))  or
                self.__right_collider.arrived(self.__x_pos, self.__y_pos)
            ):
            self.__x_pos, self.__y_pos = self.__left_collider.center() if  buff else self.__right_collider.center()
            self.__x_off = 0

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
                    self.__brush.down()
                    if  (   self.__end_slider.is_active() and
                            self.__end_slider.collidepoint(global_x, global_y, event.pos)
                        ):
                        if self.__y_pos <= -SCREEN_H * 2 + percetage(SCREEN_H, 5):
                            self.__end_slider.move_to("CANVAS", 8)
                            self.__y_off = 8
                        else :
                            self.__end_slider.move_to("END", -8)
                            self.__y_off = -8

                if self.__center_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__y_pos >= 0:
                        self.__y_off = -8
                        self.__center_collider.move_to("CANVAS", -8)
                    else:
                        self.__y_off = 8
                        self.__center_collider.move_to("TABLE", 8)
                elif self.__right_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__x_pos >= 0:
                        self.__x_off = -8
                        self.__right_collider.move_to("ATTEMPTS", -8)
                    else:
                        self.__x_off = 8
                        self.__right_collider.move_to("TABLE", 8)
                elif self.__left_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__x_pos <= 0:
                        self.__x_off = 8
                        self.__left_collider.move_to("INVENTAR", 8)
                    else:
                        self.__x_off = -8
                        self.__left_collider.move_to("TABLE", -8)
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
                self.__player.deacrease_health(amount = self.__difficultie.health_drain() * delta_time)
                self.__player.display_dripping(self.__screen, delta_time, self.__x_pos, self.__y_pos) #deffinietly not 30FPS but looks dope
                print(self.__player.health())
                pygame.image.save(a_canvas[0], "profile/input/char" + str(a_canvas[2]) + ".png") #Preanswer guessing
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__canvases.save()
                answer = self.__evaluator.make_string(True) #Finall Answer guessing
                if (likness := self.__table.check_solution(answer))[0]:
                    self.__end_slider.activate()
                else:
                    self.__canvases = canvas.CCanvases(SCREEN_H)
                    self.__attempts.add((answer, likness[1]))


        return True


if __name__ == "__main__":
    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    level = CLevel("MEDIUM")
    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = level.display_level(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
