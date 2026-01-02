"""
Script that generates menu
"""
import pygame
from tools.anim_button import CAnimButton, CAnimations
from tools.shop import CShop
from tools.button      import CButton

SCREEN_W = 1024 # 4 x 3
SCREEN_H = 768

#WIZ_IDLE  500x500
#WIZ_HOVER 500x500


class CMenu():
    """
    Class for handling menu
    """
    def __init__(self, manager):
        self.__manager = manager

        self.__screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

        self.__quit = False

        temp_pos = (0,0)
        off_set  = 50

        self.__board = pygame.image.load("assets/bounty_board.png")

        self.__shop = CShop(self.__manager.player, SCREEN_H)

        self.__easy     = CButton(  position = temp_pos,
                                    idle = "assets/difficultie_posters/EASY_idle.png",
                                    pressed = "assets/difficultie_posters/EASY_pressed.png",
                                    on_press = lambda : self.inspect_contact(self.__easy),
                                )
        self.__medium   = CButton(  position = temp_pos,
                                    idle = "assets/difficultie_posters/MEDIUM_idle.png",
                                    pressed = "assets/difficultie_posters/MEDIUM_pressed.png",
                                    on_press = lambda : self.inspect_contact(self.__medium),
                                    )
        self.__hard   = CButton(    position = temp_pos,
                                    idle = "assets/difficultie_posters/HARD_idle.png",
                                    pressed = "assets/difficultie_posters/HARD_pressed.png",
                                    on_press = lambda : self.inspect_contact(self.__hard),
                                    )

        self.__wizzad = CAnimButton(pos = (SCREEN_W , SCREEN_H),
                                    idle = CAnimations("assets/wiz_idle", fps = 5),
                                    hovered= CAnimations("assets/wiz_hover", fps = 5),
                                    pressed= CAnimations("assets/wiz_pres", fps=5),
                                    on_press = self.start_shoping,
                                    on_release= self.exit_shoping)


        self.__decline = CButton(   position = temp_pos,
                                    idle = "assets/decline.png",
                                    active = False,
                                    on_press = self.refuse_contract,
                                    on_release= self.refuse_contract,
                                    visible = False
                                )
        self.__accept = CButton(    position= temp_pos,
                                    idle= "assets/accept.png",
                                    active = False,
                                    on_press = self.accept_contract,
                                    on_release= self.accept_contract,
                                    visible = False
                                )

        self.__leave = CButton(  position    = temp_pos,
                                 idle        = "assets/decline.png",
                                 width       = 75,
                                 height      = 75,
                                 active      = True,
                                 visible     = True,
                                 on_press    = self.leave
                             )

        self.__easy.move((250, SCREEN_H - 1.5 * self.__easy.height()))
        self.__medium.move((450, SCREEN_H - 2 * self.__medium.height()))

        temp_pos = self.__center_align((self.__hard.width(), self.__hard.height()))
        self.__hard.move((temp_pos[0], 100))
        self.__decline.move((SCREEN_W//2 - self.__decline.width(), SCREEN_H - self.__decline.height() - off_set))
        self.__accept.move(((SCREEN_W//2, SCREEN_H - self.__accept.height() - off_set)))
        self.__leave.move((SCREEN_W - self.__leave.width(), 0))

        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

        self.__orig_pos = (0, 0)
        pygame.time.delay(25)

    def display(self, delta_time):
        """
        Method for displaying menu,
        intended to be called in 
        main game_loop 
        """
        if self.__quit: #Player pressed leave button
            return False

        self.__screen.fill((0,0,0))
        self.handle_events()

        if self.__wizzad.state(): #opened shop
            self.__shop.activate()
            self.__shop.display(self.__screen)

        else:
            self.__shop.deactivate()
            self.__screen.blit(self.__board, self.__center_align((self.__board.get_width(), self.__board.get_height())))

        self.__wizzad.display(self.__screen, 0, 0, delta_time)

        self.__easy.display(self.__screen, 0, 0)
        self.__medium.display(self.__screen, 0, 0)
        self.__hard.display(self.__screen, 0, 0)


        self.__decline.display(self.__screen, 0, 0)
        self.__accept.display(self.__screen, 0, 0)

        self.__leave.display(self.__screen, 0, 0)
        return True

    def handle_events(self) -> bool:
        """
        Method for handling events 
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave()

    def start_shoping(self):
        """
        Metod for shoping with wizzard
        """
        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

        self.__call_on_buttons("deactivate", [self.__easy, self.__medium, self.__hard])
        self.__call_on_buttons("hide", [self.__easy, self.__medium, self.__hard])


    def exit_shoping(self):
        """
        Metod for extting shop with wizzard
        """
        self.__wizzad.right_bottom((SCREEN_W, SCREEN_H))

        self.__call_on_buttons("activate", [self.__easy, self.__medium, self.__hard])
        self.__call_on_buttons("show", [self.__easy, self.__medium, self.__hard])

    def inspect_contact(self, contract : CButton):
        """
        Moves contract to center of screen
        """
        pos = self.__center_align((contract.width("pressed"), contract.height("pressed")))
        self.__orig_pos = contract.postion()
        contract.move(pos)

        self.__call_on_buttons("deactivate", [self.__easy, self.__medium, self.__hard, self.__wizzad])
        self.__call_on_buttons("hide", [self.__easy, self.__medium, self.__hard], [contract])
        self.__call_on_buttons("show", [self.__accept, self.__decline])
        self.__call_on_buttons("activate", [self.__accept, self.__decline])

        self.__active_contract = contract

    def refuse_contract(self):
        """
        Moves contract to original postion
        """
        self.__active_contract.move(self.__orig_pos)
        self.__active_contract.make_idle()

        self.__call_on_buttons("activate", [self.__easy, self.__medium, self.__hard, self.__wizzad])
        self.__call_on_buttons("show", [self.__easy, self.__medium, self.__hard])
        self.__call_on_buttons("hide", [self.__accept, self.__decline])
        self.__call_on_buttons("deactivate", [self.__accept, self.__decline])

    def accept_contract(self):
        """
        Changes Scene to desired 
        level
        """
        match self.__active_contract:
            case self.__easy:
                self.__call_on_buttons("clean", [self.__easy, self.__medium, self.__hard, self.__wizzad, self.__accept, self.__decline])
                self.__manager.change_scene(self.__manager, "EASY")
            case self.__medium:
                self.__call_on_buttons("clean", [self.__easy, self.__medium, self.__hard, self.__wizzad, self.__accept, self.__decline])
                self.__manager.change_scene(self.__manager, "MEDIUM")
            case self.__hard:
                self.__call_on_buttons("clean", [self.__easy, self.__medium, self.__hard, self.__wizzad, self.__accept, self.__decline])
                self.__manager.change_scene(self.__manager, "HARD")

    def leave(self):
        """
        Leave game using leave button
        """
        self.__manager.player.save()
        self.__quit = True

    def __center_align(self, size):
        """
        find center cordinates for given surf
        """
        pos = (SCREEN_W // 2 - size[0]//2, SCREEN_H // 2 - size[1]//2)
        return pos

    def __call_on_buttons(self, method, buttons, skip = None):
        """
        Iterates throught buttons and
        hides them
        """
        for button in buttons:
            if skip is not None and button in skip:
                continue
            getattr(button, method)()
        pygame.time.delay(25)

if __name__ == "__main__":
    from scenes.scene_manager import CSceneManager

    RUNNING  = True
    DELTA_TIME = 0.1

    pygame.init()
    clock = pygame.time.Clock()

    menu = CMenu(CSceneManager())

    while RUNNING:

        RUNNING = menu.display(DELTA_TIME)

        pygame.display.flip()

        DELTA_TIME = clock.tick(60) / 1000 #tick is in ms
        DELTA_TIME = max(0.1, min(0.1, DELTA_TIME))
    pygame.quit()
