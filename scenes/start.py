"""
Start_up menu 
"""
import pygame
from tools.button import CButton

SCREEN_W = 500
SCREEN_H = 500

class CStart():
    """
    Class for displaying and handling Start_up scene
    """
    def __init__(self, manager, path = "profile/player.txt"):
        self.__manager = manager
        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.__path = path

        self.__reset = False

        temp_pos = (0, 0)

        self.__new_game = CButton(
            position = (0, 0),
            idle = "assets/start_up/new_game.png",
            on_press = self.new_game
        )
        self.__continue = CButton(
            position = (0, SCREEN_H // 2),
            idle = "assets/start_up/continue.png",
            on_press = self.scene_to_menu
        )

        self.__accept = CButton(
            position = temp_pos,
            idle = "assets/accept.png",
            width = 50,
            height = 50,
            active = True,
            visible = True,
            on_press = self.accept
        )

        self.__decline = CButton(
            position = temp_pos,
            idle = "assets/decline.png",
            width = 50,
            height = 50,
            active = True,
            visible = True,
            on_press = self.decline
        )


        try:
            with open(self.__path, mode = "r", encoding = "utf-8"):
                self.__exist = True

        except FileNotFoundError:
            self.__exist = False
            self.__continue.deactivate()
            self.__continue.hide()


    def display(self, __delta_time):
        """
        Method for displaying Scene in Game_loop
        """
        self.__screen.fill((0,0,0))

        continue_looping = self.__event_handler()

        if self.__exist and self.__reset:
            font_size = 13
            font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
            text = "Do you want to overwrite existing Save ?"
            question = font.render(text, True, (255, 255, 255))
            size = question.get_rect().size

            question_top_left = (SCREEN_W//2 - size[0]//2, SCREEN_H//2 - size[1]//2)

            self.__accept.move(
                (SCREEN_W//2 - self.__accept.width(), question_top_left[1] + size[1])
            )
            self.__decline.move((SCREEN_W//2, question_top_left[1] + size[1]))

            self.__screen.blit(question, question_top_left)
            self.__accept.display(self.__screen, 0, 0)
            self.__decline.display(self.__screen, 0, 0)
            return continue_looping


        self.__new_game.display(self.__screen, 0, 0)
        self.__continue.display(self.__screen, 0, 0)

        return continue_looping

    def __event_handler(self):
        """
        Method for handling events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def scene_to_menu(self):
        """
        Change Scene to menu
        """

        while pygame.mouse.get_pressed()[0]:
            pygame.event.get()

        self.__manager.change_scene(self.__manager, "MENU")
        return "MENU"

    def accept(self):
        """
        Change Scene to menu and resets 
        Player stats
        """
        base_stats = "200\n0"
        with open(self.__path, mode = "w", encoding = "utf-8") as f:
            f.write(base_stats)
        self.__manager.player.refresh_stats()
        self.scene_to_menu()

        self.__reset = True

    def new_game(self):
        """
        Method for accept button
        """
        if not self.__exist:
            self.accept()

        self.__reset = True

        self.__new_game.deactivate()
        self.__continue.deactivate()

    def decline(self):
        """
        Method for decline button
        """
        self.__reset = False

        self.__new_game.activate()
        self.__continue.activate()

        self.__new_game.make_idle()
        self.__decline.make_idle()

        while pygame.mouse.get_pressed()[0]:
            pygame.event.get()


if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING = True
    DELTA_TIME = 0.1

    pygame.init()
    t_manager = CSceneManager()
    t_manager.change_scene(t_manager, "START")
    clock = pygame.time.Clock()

    while RUNNING:

        RUNNING = t_manager.scene.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
