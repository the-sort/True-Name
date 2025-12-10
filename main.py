"""
This script runs main game_loop
"""
import pygame
import tools.table_generator as tg
from tools.utils import percetage

# 32 x 32
# 16 x 16
#  8 x 8
if __name__ == "__main__":

    RUNNING  = True
    SCREEN_W = 1024 # 4 x 3
    SCREEN_H = 768
    COLS     = 16
    ROWS     = 12

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    table = tg.CTable(screen, "EASY", "ENG")

    bottom_place_holder = pygame.Rect(percetage(SCREEN_W, 10), SCREEN_H - percetage(SCREEN_H, 5),  SCREEN_W - 2 * percetage(SCREEN_W, 10),  percetage(SCREEN_H, 5))
    left_place_holder  = pygame.Rect(0, 0, percetage(SCREEN_W, 5), SCREEN_H)
    right_place_holder  = pygame.Rect(SCREEN_W - percetage(SCREEN_W, 5), 0, percetage(SCREEN_W, 5), SCREEN_H)

    table.generate_windows()

    while RUNNING:
        pygame.draw.rect(screen, (255,255,255), bottom_place_holder)
        pygame.draw.rect(screen, (255,255,255), left_place_holder)
        pygame.draw.rect(screen, (255,255,255), right_place_holder)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
        pygame.display.flip()
    pygame.quit()
