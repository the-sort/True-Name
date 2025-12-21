"""
Script that generates menu
"""
import pygame

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

class CMenu:
    """
    Class for handling menu
    """
    def __init__(self):
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def display_menu(self):
        """
        Method for displaying menu,
        intended to be called in 
        main game_loop 
        """
        self.__screen.fill((0,0,0))
        continue_looping = self.handle_events()

        return continue_looping

    def handle_events(self) -> bool:
        """
        Method for handling events 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True




if __name__ == "__main__":
    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    clock = pygame.time.Clock()

    menu = CMenu()

    while RUNNING:

        RUNNING = menu.display_menu()

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
