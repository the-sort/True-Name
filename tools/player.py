"""
Helper module containing Player class
"""
import pygame
from tools.animator import CAnimations

class CPlayer:
    """
    Class for player to handle 
    his stats and inventar
    """

    def __init__(self):
        try:
            with open("profile/player.txt", mode = "r", encoding = "utf-8") as f:
                self.__health = self.__full_health = int(f.readline())
                self.__coins = int(f.readline())
        except (FileNotFoundError, PermissionError):
            self.__health = self.__full_health = 200
            self.__coins = 0

        transform = (150, 150)
        self.__health_vial = pygame.image.load("assets/health_vial_empty.png")
        self.__health_vial = pygame.transform.scale(self.__health_vial, transform)
        self.__health_vial_blood = pygame.image.load("assets/health_vial_blood.png")
        self.__health_vial_blood = pygame.transform.scale(self.__health_vial_blood, transform)

        self.__health_vial_animation = CAnimations(path = "assets/dripping", fps = 30)
        self.__health_vial_animation.rescale(transform)

        self.__full_height = self.__health_vial_blood.get_rect().height
        self.__full_width = self.__health_vial_blood.get_rect().width
        self.__full_vial_blood = self.__health_vial_blood

    def display_health(self, screen: pygame.Surface, global_x, global_y):
        """
        Metod used for displaying
        actual health state of player
        """

        size = screen.get_rect().size

        top_left = (75 + global_x, size[1] + global_y)
        top_right = (-75 + size[0] + global_x -  self.__full_width, size[1] + global_y)

        screen.blit(self.__health_vial_blood, top_left)
        screen.blit(self.__health_vial_blood, top_right)

        screen.blit(self.__health_vial, top_left)
        screen.blit(self.__health_vial, top_right)

    def display_dripping(self, screen, delta_time, global_x, global_y):
        """
        Plays dripping animation
        """
        size = screen.get_rect().size

        top_left = (75 + global_x, size[1] + global_y)
        top_right = (-75 + size[0] + global_x -  self.__full_width, size[1] + global_y)

        self.__health_vial_animation.play(
            screen,
            delta_time,
            (top_left[0], top_left[1] + self.__full_height)
        )
        self.__health_vial_animation.play(
            screen,
            delta_time,
            (top_right[0], top_right[1] + self.__full_height)
        )

    def deacrease_health(self, amount=-1):
        """
        Metod for deacreasing player health
        When amount is >=0 does nothing
        """
        if amount >= 0:
            return

        self.__health += amount

        transform = self.__health_vial_blood.get_rect().size
        transform = (transform[0], abs(self.__full_height*self.__health/self.__full_health))

        self.__health_vial_blood = pygame.transform.scale(self.__health_vial_blood, transform)

    def increase_health(self, amount=1):
        """
        Metod for increasing player health
        When amount is <=0 does nothing
        """
        if amount <= 0:
            return

        self.__health += amount

    def increase_full_health(self, amount=1):
        """
        Metod for increasing player health
        When amount is <=0 does nothing
        """
        if amount <= 0:
            return

        self.__full_health += amount


    def health(self) -> float:
        """
        Getter for atribute health
        """
        return self.__health

    def full_health(self):
        """
        Getter for for atribute full health
        """
        return self.__full_health

    def coins(self):
        """
        Returns how many Coins does player
        have
        """
        return self.__coins

    def add_coins(self, amount):
        """
        Adds amount of coins to player
        """
        if amount <= 0:
            raise ValueError("Insuffiecient amount of coins")

        self.__coins += amount

    def substract_coins(self, amount):
        """
        Substracts amount of coins from player
        """
        if amount <= 0:
            raise ValueError("Insuffiecient amount of coins")

        self.__coins -= amount

    def heal_to_full(self):
        """
        Restores health to full
        """
        self.__health = self.__full_health + 1
        self.__health_vial_blood = self.__full_vial_blood

    def save(self):
        """
        Save player stats
        """
        to_save = str(self.__full_health) + "\n" + str(self.__coins)
        with open("profile/player.txt", mode = "w", encoding = "utf-8") as f:
            f.write(to_save)

    def refresh_stats(self):
        """
        Refreshes stats from file
        """
        try:
            with open("profile/player.txt", mode = "r", encoding = "utf-8") as f:
                self.__health = self.__full_health = int(f.readline())
                self.__coins = int(f.readline())
        except (FileNotFoundError, PermissionError):
            self.__health = self.__full_health = 200
            self.__coins = 0

if __name__ == "__main__":
    ...
