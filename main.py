"""
This script runs main game_loop
"""
import pygame
import tools.table_generator as tg


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    table = tg.CTable(32,32, "SK")
    font = pygame.font.Font(None, 36)

    RUNNING = True

    table = [["1","2","3"],["4","5","6"],["7","8","9"]]
    screen.fill((0,0,0))
    x = 50
    y = 50
    for lines in table:
        line = font.render(str(lines), True, (255,255,255))
        screen.blit(line, (x,y))
        x += 40
        y += 40
        x = 50 
    pygame.display.flip()
    
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
    pygame.quit()
