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

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

class CLevel:
    """
    Metods for handling level
    """
    def __init__(self, difficultie, language = "ENG"):
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__table  = tg.CTable(self.__screen, difficultie, language)
        self.__attempts = attempts.CAttempts(self.__screen)

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

    def display_level(self):
        """
        Metod called in game loop
        """

        self.__screen.fill((0,0,0))
        self.__table.display_table(self.__x_pos, self.__y_pos)

        self.__canvases.display_canvases(self.__screen, self.__x_pos, self.__y_pos)
        self.__attempts.display_attempts(self.__x_pos, self.__y_pos)


        self.__center_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__left_collider.display_slider(self.__x_pos, self.__y_pos)
        self.__right_collider.display_slider(self.__x_pos, self.__y_pos)

        continue_looping = self.__event_handler(self.__x_pos, self.__y_pos)


        self.__x_pos += self.__x_off
        self.__y_pos += self.__y_off

        if  self.__y_pos <= -SCREEN_H + percetage(SCREEN_H, 5) or self.__y_pos >= 0:
            self.__y_off = 0

        if  (   self.__x_pos <= -SCREEN_W + percetage(SCREEN_W, 5)  or
                self.__x_pos >= SCREEN_W - percetage(SCREEN_W, 5)   or
                self.__x_pos == 0
            ):
            self.__x_off = 0


        return continue_looping

    def __event_handler(self, global_x, global_y):
        """
        Metod handling all inputs and events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    self.__brush.down()
                    # last_pos = event.pos

                if self.__center_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__y_pos >= 0:
                        self.__y_off = -8
                    else:
                        self.__y_off = 8
                elif self.__right_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__x_pos >= 0:
                        self.__x_off = -8
                    else:
                        self.__x_off = 8
                elif self.__left_collider.collidepoint(global_x, global_y, event.pos):
                    if self.__x_pos <= 0:
                        self.__x_off = 8
                    else:
                        self.__x_off = -8
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   # left click
                    self.__brush.up()
                    # last_pos = event.pos
            if event.type == pygame.MOUSEMOTION and self.__brush.is_down():
                if (a_canvas := self.__canvases.get_active(event.pos)) is None:
                    continue
                self.__brush.draw(a_canvas[0], a_canvas[1], event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__canvases.save()
                answer = self.__evaluator.make_string()
                if (likness := self.__table.check_solution(answer))[0]:
                    print("GOOD JOB!")
                else:
                    self.__canvases = canvas.CCanvases(SCREEN_H)
                    self.__attempts.add((answer, likness[1]))
                    print(likness[1])


        return True


if __name__ == "__main__":
    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    level = CLevel("MEDIUM")
    clock = pygame.time.Clock()

    while RUNNING:
        RUNNING = level.display_level()

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
