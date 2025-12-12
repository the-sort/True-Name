"""
Script creates level 
"""
import pygame
from tools.utils import percetage
import tools.table_generator as tg

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

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
        pixel = pygame.Rect(pos[0] - canvas_rect.x , pos[1] - canvas_rect.y, self.__size, self.__size)
        pygame.draw.rect(canvas, self.__color, pixel)


class CCanvases:
    """
    Class for handling players drawings
    """
    def __init__(self):
        self.__width            = 175
        self.__height           = 175
        self.__canvases         = [pygame.Surface((self.__width,self.__height)) for _ in range(10)]
        self.__canvases_rect    = [canvas.get_rect() for canvas in self.__canvases]

        for canvas in self.__canvases:
            canvas.fill((255,255,255))
    
    def display_canvases(self, screen, global_x, global_y):
        """
        Metod used for displaying canvases
        """
        x_offset = 74
        for i in range(5):
            l_corner = (x_offset + global_x, (SCREEN_H//2) + SCREEN_H + global_y - self.__height)
            screen.blit(self.__canvases[i], l_corner)
            self.__canvases_rect[i] = self.__canvases[i].get_rect(topleft = l_corner)
            x_offset += 175

        x_offset = 74
        for i in range(5,10):
            l_corner = (x_offset + global_x, (SCREEN_H//2) + SCREEN_H + global_y)
            screen.blit(self.__canvases[i], l_corner)
            self.__canvases_rect[i] = self.__canvases[i].get_rect(topleft = l_corner)
            x_offset += 175
    def get_active(self, pos):
        """
        Metod that returns canvas with 
        which player interacts
        Return None if interacts with nothing
        Return Surface and rect when found
        """
        for i in enumerate(self.__canvases):
            if self.__canvases_rect[i[0]].collidepoint(pos):
                return (i[1],self.__canvases_rect[i[0]])
        return None





class CLevel:
    """
    Metods for handling level
    """
    def __init__(self, difficultie, language = "ENG"):
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__table  = tg.CTable(self.__screen, difficultie, language)
        # self.__canvas = pygame.Surface((175,175))

        self.__x_pos    = 0
        self.__y_pos    = 0
        self.__x_off    = 0
        self.__y_off    = 0

        self.__canvases = CCanvases()
        self.__brush = CBrush()
        
    def display_level(self):
        """
        Metod called in game loop
        """

        self.__screen.fill((0,0,0))
        self.__table.display_table(self.__x_pos, self.__y_pos)

        # self.__screen.blit(self.__canvas, (74 + self.__x_pos, (SCREEN_H//2) + SCREEN_H + self.__y_pos))
        # self.__canvas_rect = self.__canvas.get_rect(topleft = (74 + self.__x_pos, (SCREEN_H//2) + SCREEN_H + self.__y_pos))
        self.__canvases.display_canvases(self.__screen, self.__x_pos, self.__y_pos)

        center_collider  = pygame.Rect  (   percetage(SCREEN_W, 10) + self.__x_pos            ,
                                            SCREEN_H - percetage(SCREEN_H, 5) + self.__y_pos  ,
                                            SCREEN_W - 2 * percetage(SCREEN_W, 10)            ,
                                            percetage(SCREEN_H, 5)
                                            )
        left_collider    = pygame.Rect  (   0 + self.__x_pos        ,
                                            0 + self.__y_pos        ,
                                            percetage(SCREEN_W, 5)  ,
                                            SCREEN_H
                                            )
        right_collider   = pygame.Rect  (   SCREEN_W - percetage(SCREEN_W, 5) + self.__x_pos ,
                                            0 + self.__y_pos                                 ,
                                            percetage(SCREEN_W, 5)                           ,
                                            SCREEN_H
                                            )

        pygame.draw.rect(self.__screen, (255,255,255),center_collider)
        pygame.draw.rect(self.__screen, (255,255,255),left_collider)
        pygame.draw.rect(self.__screen, (255,255,255),right_collider)

        continue_looping = self.__event_handler(center_collider, left_collider, right_collider)


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

    def __event_handler(self, center_collider, left_collider, right_collider):
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

                if center_collider.collidepoint(event.pos):
                    if self.__y_pos >= 0:
                        self.__y_off = -8
                    else:
                        self.__y_off = 8
                elif right_collider.collidepoint(event.pos):
                    if self.__x_pos >= 0:
                        self.__x_off = -8
                    else:
                        self.__x_off = 8
                elif left_collider.collidepoint(event.pos):
                    if self.__x_pos <= 0:
                        self.__x_off = 8
                    else:
                        self.__x_off = -8
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:   # left click
                    self.__brush.up()
                    # last_pos = event.pos
            if event.type == pygame.MOUSEMOTION and self.__brush.is_down():
                # print(self.__canvas.get_rect().collidepoint)
                if (canvas := self.__canvases.get_active(event.pos)) is None:
                    continue
                self.__brush.draw(canvas[0], canvas[1], event.pos)

        return True

    # def __del__(self):
    #     pygame.image.save(self.__canvas, "Char.png")


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
