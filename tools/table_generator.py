"""
Tool designed to generate table of custom dimension
and fill it with random words from dictionary
"""
import warnings
import random

MAX_WORD_LEN = 15
MIN_WORD_LEN = 3

class CTable:
    """
    table filled with random words
    """
    def __init__(self, cols, rows, language):
        self.__cols = cols
        self.__rows = rows
        self.__table = [["" for j in range(self.__cols)] for i in range(self.__rows)]
        self.__dictionary = [[] for _ in range(MAX_WORD_LEN + 1)]

        self.__read_dict(language)
        self.__solution = self.__fill_table()
        # for line in self.__table:
        #     print(line)
        # print(self.__table)
        # print(self.__solution)

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
        chars = "()~!@#$%^&*()_+/*-{}|:<>?`"
        if am_chars == 0:
            am_chars = random.randint(1, self.__cols - index)
        for _ in range(am_chars):
            row[index] = random.choice(chars)
            index += 1
        return index




if __name__ == "__main__":
    table = CTable(16, 16, "ENG")
    while True:
        guess = input("Guess word in table: ")
        alike = table.check_solution(guess)
        if alike[0]:
            break
        print(guess, " , likness: ", alike[1])
