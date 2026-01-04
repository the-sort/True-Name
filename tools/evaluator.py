"""
Tool which uses pretrained pytorch
model to convert user drawn picture
and compare it to given string
"""

import json
import torch
import torchvision.transforms as transforms
from PIL import Image
import pygame
from tools.translator import CSimpleLetterClassifier
from tools.utils import is_blank
from tools.slider import SLIDER_H

class CEvaluator:
    """
    class used for evalutating user drawn picture
    """

    def __init__(self, path="profile/input/", clean_up=True):
        self.__set_model()
        self.__images = []
        self.__guess = ""
        self.__changed = False
        self.__path = path

        self.__class_to_index = self.__assign_index()
        if clean_up:
            self.__clean_input()

    def __assign_index(self):
        """
        Assign letter to index
        """
        with open("dictionaries/classes.json", "r", encoding="utf-8") as f:
            classes = json.load(f)
        return classes


    def __set_model(self):
        """
        Initializes pretrained model
        """
        self.__device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model = CSimpleLetterClassifier().to(self.__device)
        self.__model.load_state_dict(torch.load(
                                        "model1.pth", 
                                        weights_only=True,
                                        map_location =
                                            "cuda:0" if torch.cuda.is_available()
                                            else "cpu"
                                    )
        )
        self.__model.eval()

    def __preproces_input(self):
        """
        Preproces users drawing for model
        """
        self.__images = []
        transform = transforms.Compose(
            [transforms.Resize((128, 128)), transforms.ToTensor()]
        )

        for i in range(10):
            try:
                img = Image.open(self.__path + f"char{i}.png").convert("L").convert("RGB")
            except FileNotFoundError:
                img = Image.open("assets/blank.png").convert("L").convert("RGB")
            if is_blank(image = img, background = (255, 255, 255)):
                continue
            self.__images.append(transform(img).unsqueeze(0))

    def __clean_input(self):
        """
        Saves all chars in profile/input as blanks
        """
        img = Image.open("assets/blank.png").convert("L").convert("RGB")
        for i in range(10):
            img.save(self.__path + f"char{i}.png")
        # print("Saving Evaluator")
        self.__guess = ""


    def make_string(self, cleanup = True) -> str:
        """
        Checks if users word matches given word
        """
        self.__preproces_input()
        answer = ""
        for letter in self.__images:
            with torch.no_grad():
                letter = letter.to(self.__device)
                prediction = self.__model(letter)
                probabilities = torch.nn.functional.softmax(prediction, dim = 1)
                pred_idx = probabilities.argmax(dim=1).item()
                class_name = self.__class_to_index[pred_idx]
                answer += class_name.capitalize()
        if cleanup:
            self.__clean_input()
        return answer

    def changed(self):
        """
        Indicates that player added new letter
        to string
        """
        self.__changed = True

    def guess(self, screen, global_x, global_y):
        """
        Displays what has model temporarly
        evaluated
        """
        if self.__changed:
            self.__guess = self.make_string(False)
            self.__changed = False
        font_size = 25
        color = (255, 255, 255)
        font = pygame.font.Font("./dictionaries/Gothic_pixel_font_fixed.ttf", font_size)
        guess_surface = font.render(self.__guess, True, color)
        guess_pos = (
            (screen.get_width() // 2) - (guess_surface.get_width()/2) + global_x,
            screen.get_height() + SLIDER_H  - guess_surface.get_height()//1.5 + global_y
        )
        screen.blit (guess_surface, guess_pos)








if __name__ == "__main__":
    evaluator = CEvaluator()
    evaluator.make_string()
