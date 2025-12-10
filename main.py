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
    DELTA_TIME = 0.1
    SCREEN_W = 1024 # 4 x 3
    SCREEN_H = 768
    COLS     = 16
    ROWS     = 12

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    table = tg.CTable(screen, "EASY", "ENG")

    bottom_place_holder = pygame.Rect(percetage(SCREEN_W, 10), SCREEN_H - percetage(SCREEN_H, 5),  SCREEN_W - 2 * percetage(SCREEN_W, 10),  percetage(SCREEN_H, 5))
    left_place_holder  = pygame.Rect(0, 0, percetage(SCREEN_W, 5), SCREEN_H)
    right_place_holder  = pygame.Rect(SCREEN_W - percetage(SCREEN_W, 5), 0, percetage(SCREEN_W, 5), SCREEN_H)

    # table.generate_windows()
    # global_x = 0
    global_y = 0
    is_on_top = False
    off = 0

    while RUNNING:
        screen.fill((0,0,0))
        table.display_table(global_y = global_y)

        bottom_place_holder = pygame.Rect(percetage(SCREEN_W, 10), SCREEN_H - percetage(SCREEN_H, 5) + global_y,  SCREEN_W - 2 * percetage(SCREEN_W, 10),  percetage(SCREEN_H, 5))
        pygame.draw.rect(screen, (255,255,255), bottom_place_holder)
        # pygame.draw.rect(screen, (255,255,255), left_place_holder)
        # pygame.draw.rect(screen, (255,255,255), right_place_holder)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bottom_place_holder.collidepoint(event.pos) and global_y == 0:
                    off = -8
                elif bottom_place_holder.collidepoint(event.pos):
                    off = 8
                # print(bottom_place_holder.collidepoint(event.pos))
        global_y += off

        if global_y <= -SCREEN_H + percetage(SCREEN_H, 5) and not is_on_top:
            off = 0
            is_on_top = True
        elif global_y >= 0 and is_on_top:
            off = 0
            is_on_top = False
        print(global_y)
        pygame.display.flip()
        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
