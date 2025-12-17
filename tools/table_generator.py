"""
Tool designed to generate table of custom dimension
and fill it with random words from dictionary
HARD   =  16 x 12
MEDIUM =  8  x 6
EASY   =  6  x 5
"""
import warnings
import random
import pygame
from tools.utils import percetage
from tools.utils import CDificulties

MAX_WORD_LEN = 15
MIN_WORD_LEN = 3



class CTable:
    """
    table filled with random words
    """
    def __init__(self, screen, difficultie : CDificulties, language):
        self.__set_dim(difficultie)

        self.__screen = screen
        self.__table = [["" for j in range(self.__cols)] for i in range(self.__rows)]
        self.__dictionary = [[] for _ in range(MAX_WORD_LEN + 1)]

        self.__read_dict(language)
        self.__solution = self.__fill_table()
        # for line in self.__table:
        #     print(line)

    def check_solution(self, guessed_word) -> tuple:
        """
        Compares guessed word with generated
        returns True if they are same
        else returns amount of same characters
        """
        if self.__solution == guessed_word:
            return (True, 0)

        likeness = 0
        word_len = min(len(self.__solution), len(guessed_word))

        for i in range(word_len):
            if self.__solution[i] == guessed_word[i]:
                likeness += 1
        return (False, likeness)

    def display_table(self, global_x = 0, global_y = 0):
        """
        Metod used to display table
        """
        screen_center = pygame.Rect (
                            percetage(self.__screen.get_width(), 5),
                            0,
                            self.__screen.get_width() - 2 * percetage(self.__screen.get_width(), 5),
                            self.__screen.get_height() -  percetage(self.__screen.get_height(), 5)
                                    )
        window = pygame.image.load("window.png")
        window = pygame.transform.scale (window, (   window.get_width() * self.__scale,
                                                    window.get_height() * self.__scale )
                                        )

        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", self.__font_size)

        y = (screen_center.centery - (window.get_height() * self.__rows // 2)) + global_y
        for line in self.__table:
            x = (screen_center.centerx - (window.get_width() * self.__cols //2)) + global_x
            for col in line:
                col_surface = font.render(col, True, (255,255,255))
                x_off = (window.get_width() - col_surface.get_width()) // 2
                y_off = (window.get_height() - col_surface.get_height()) //2
                self.__screen.blit(window,(x,y))
                self.__screen.blit(col_surface, (x + x_off ,y + y_off))
                x += window.get_width()
            y += window.get_height()

    def health_drain(self):
        """
        Metod that returns how much
        health should be drained
        from player
        """
        return self.__health_drain

    def __set_dim(self, difficultie : CDificulties):
        """
        Sets dimension and scales of table
        """
        self.__cols         = difficultie.cols()
        self.__rows         = difficultie.rows()
        self.__scale        = difficultie.scale()
        self.__font_size    = difficultie.font_size()


    def __read_dict(self, language) -> None:
        """
        Reads content of desired dictionary
        """
        path = "dictionaries/" + language + "_edited.txt"
        try:
            with open(path, mode = "rt", encoding = "utf-8") as source:
                for line in source.readlines():
                    line = line.removesuffix("\n")
                    self.__dictionary[len(line)].append(line)
        except FileNotFoundError:
            warnings.warn("Desired language was not found. Language set to English")
            with open("dictionaries/ENG_edited.txt", mode = "rt", encoding = "utf-8") as source:
                for line in source.readlines():
                    line = line.removesuffix("\n")
                    self.__dictionary[len(line)].append(line)

    def __fill_table(self) -> str:
        """
        fill table with random words and chars
        """
        possible_solutions = []
        for row in self.__table:
            index = 0
            while index < self.__cols:
                num = random.randint(0,10)
                if self.__cols - index < 3:
                    index = self.__put_chars(row, index, self.__cols - index)
                    break
                if num  % 2 == 0 or num % 3 == 0:
                    index = self.__put_word(row, possible_solutions, index)
                else:
                    index = self.__put_chars(row, index)
        return possible_solutions[random.randint(0, len(possible_solutions) - 1)]



    def __put_word(self, row : list, possible_solutions : list, index : int) -> int:
        """
        puts word into given row
        """
        try:
            word_len = random.randint(MIN_WORD_LEN,  min(self.__cols - index - 1, MAX_WORD_LEN))
        except ValueError:
            word_len = 3
        word = self.__dictionary[word_len][random.randint(0, len(self.__dictionary[word_len]) - 1)]
        possible_solutions.append(word)
        for char in word:
            row[index] = char
            index += 1
        return index

    def __put_chars(self, row : list, index : int, am_chars = 0) -> int:
        """
        puts chars into given row
        """
        # chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ"
        chars = "()~!@#$%&()_+/-{}|:<>?"
        if am_chars == 0:
            am_chars = random.randint(1, self.__cols - index)
        for _ in range(am_chars):
            row[index] = random.choice(chars)
            index += 1
        return index




if __name__ == "__main__":
    SCREEN_W = 1024 # 4 x 3
    SCREEN_H = 768
    buff = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    table = CTable(buff, "HARD", "ENG")
    while True:
        guess = input("Guess word in table: ")
        alike = table.check_solution(guess)
        if alike[0]:
            break
        print(guess, " , likness: ", alike[1])
