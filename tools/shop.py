"""
Tool for displaying and handling shop
"""
import pygame
from tools.button import CButton

class CShop:
    """
    Class for displaying and handling shop
    """
    def __init__(self, player, screen_h):
        temp_pos = (0, 0)

        self.__screen_h = screen_h

        self.__player = player
        self.__prize_int = self.__player.full_health()//2

        self.__shop_frame = pygame.image.load("assets/shop_frame.png")
        self.__coin_img = pygame.image.load("assets/coin_scaled.png")
        self.__health_img = pygame.image.load("assets/health_vial.png")

        self.__small_coin = pygame.transform.scale(self.__coin_img, (35, 35))

        self.__plus = CButton(
            position = temp_pos,
            idle = "assets/plus_button.png",
            active = False,
            visible = False,
            on_press = self.upgrade_health
        )

        self.__am_coins = self.__render_font(str(self.__player.coins()), 25)
        self.__health = self.__render_font(str(self.__player.full_health()) + "/2000", 17)
        self.__prize = self.__render_font(str(self.__prize_int), 17)

    def display(self, screen):
        """
        Method for displaying shop
        """
        off_set = 50

        shop_frame_size = self.__shop_frame.get_rect().size
        coins_size = self.__am_coins.get_rect().size
        coin_img_size = self.__coin_img.get_rect().size
        header_size = (coins_size[0] + coin_img_size[0], max(coins_size[1], coin_img_size[1]))
        health_size = self.__health.get_rect().size
        prize_txt_size = self.__prize.get_rect().size

        shop_frame_top_left = (0, self.__screen_h//2 - self.__shop_frame.get_rect().height//2)
        coins_am_top_left = (
            (
                shop_frame_top_left[0]
                + shop_frame_size[0]
                // 2
                - header_size[0]
                // 2
            ),
            shop_frame_top_left[1] + header_size[1]
        )
        health_top_left = (shop_frame_top_left[0] + off_set, coins_am_top_left[1] + 2*off_set)
        health_img_top_left = (health_top_left[0] + health_size[0], health_top_left[1])


        shop_frame_top_right = (shop_frame_size[0], shop_frame_top_left[1])
        health_top_right = (shop_frame_top_right[0], health_top_left[1])

        small_coin_top_left = (
            health_top_right[0] - self.__plus.width() - off_set,
            health_top_right[1]
        )
        prize_top_left = (
            small_coin_top_left[0] - prize_txt_size[0] - off_set//5,
            small_coin_top_left[1]
        )
        plus_top_left = (
            prize_top_left[0] - self.__plus.width() - off_set//5,
            small_coin_top_left[1]
        )

        coins_img_top_left = (
            coins_am_top_left[0] + self.__am_coins.get_width() + off_set,
            coins_am_top_left[1]
        )

        self.__plus.move(plus_top_left)

        if self.__prize_int > self.__player.coins() or self.__player.full_health() >= 2000:
            self.__plus.hide()
            self.__plus.deactivate()

        else:
            self.__plus.show()
            self.__plus.activate()

        screen.blit(self.__shop_frame, shop_frame_top_left)
        screen.blit(self.__am_coins, coins_am_top_left)
        screen.blit(self.__coin_img, coins_img_top_left)
        screen.blit(self.__health, health_top_left)
        screen.blit(self.__health_img, health_img_top_left)
        screen.blit(self.__prize, prize_top_left)
        screen.blit(self.__small_coin, small_coin_top_left)

        self.__plus.display(screen, 0, 0)

    def upgrade_health(self):
        """
        Checks if player has enough money
        then upgrades his health
        """
        if self.__prize_int > self.__player.coins() or self.__player.full_health() >= 2000:
            return

        self.__player.increase_full_health(100)
        self.__player.substract_coins(self.__prize_int)

        self.__prize_int = self.__player.full_health()//2

        self.__am_coins = self.__render_font(str(self.__player.coins()), 25)
        self.__health = self.__render_font(str(self.__player.full_health()) + "/2000", 17)
        self.__prize = self.__render_font(str(self.__prize_int), 17)

        self.__plus.make_idle()

    def activate(self):
        """
        Activates shop
        """
        self.__plus.activate()
        self.__plus.show()

    def deactivate(self):
        """
        Deactivates shop
        """
        self.__plus.deactivate()
        self.__plus.hide()



    def __render_font(self, string, font_size, color = (255, 255, 255)):
        """
        Returns rendered font
        """
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
        render = font.render(string, True, color)
        return render

if __name__ == "__main__":
    pass
