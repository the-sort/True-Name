"""
This script runs main game_loop
"""
import pygame
import scenes.level as level

# 32 x 32
# 16 x 16
#  8 x 8
if __name__ == "__main__":

    RUNNING  = True
    DELTA_TIME = 0.1
    SCREEN_W = 1024 # 4 x 3
    SCREEN_H = 768

    pygame.init()
    clock = pygame.time.Clock()
    buff = level.CLevel("MEDIUM")

    while RUNNING:
        RUNNING = buff.display_level()

        pygame.display.flip()
        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
