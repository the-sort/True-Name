import torch
import torchvision.transforms as transforms
from PIL import Image
from tools.translator import CSimpleLetterClassifier
from torchvision.datasets import ImageFolder
from tools.utils import is_blank

class CEvaluator:
    """
    class used for evalutating user drawn picture
    """

    def __init__(self):
        self.__set_model()
        self.__preproces_input()

        self.__class_to_index = {v: k for k, v in ImageFolder("dictionaries/letters/train/").class_to_idx.items()}


    def __set_model(self):
        """
        Initializes pretrained model
        """
        self.__device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.__model  = CSimpleLetterClassifier().to(self.__device)
        self.__model.load_state_dict(torch.load("model.pth", weights_only=True))
        self.__model.eval()

    def __preproces_input(self):
        """
        Preproces users drawing for model
        """
        self.__images = []
        transform = transforms.Compose  ([
                                            transforms.Resize((128, 128)),
                                            transforms.ToTensor()
                                        ])

        for i in range(10):
            img = Image.open(f"profile/input/char{i}.png").convert("L").convert("RGB")
            if is_blank(image = img, background = (255, 255, 255)):
                continue
            self.__images.append(transform(img).unsqueeze(0))

    def check_answer(self, key = ""):
        """
        Checks if users word matches given word
        """
        answer = ""
        for letter in self.__images:
            with torch.no_grad():
                letter = letter.to(self.__device)
                prediction = self.__model(letter)
                print(prediction)
                probabilities = torch.nn.functional.softmax(prediction, dim = 1)
                pred_idx = probabilities.argmax(dim=1).item()
                class_name = self.__class_to_index[pred_idx]
                answer += class_name
        print(answer)






if __name__ == "__main__":
    evaluator = CEvaluator()
    evaluator.check_answer()
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # model = CSimpleLetterClassifier().to(device)
    # model.load_state_dict(torch.load("model.pth", weights_only=True))
    # model.eval()
    # for i in range(10):
    #     img = Image.open(f"profile/input/char{i}.png").convert("L").convert("RGB")

    #     transform = transforms.Compose([
    #                 transforms.Resize((128, 128)),
    #                 transforms.ToTensor()
    #     ])
    #     img_tensor = transform(img).unsqueeze(0)

    #     with torch.no_grad():
    #         img_tensor = img_tensor.to(device)
    #         prediction = model(img_tensor)
    #         probabilities = torch.nn.functional.softmax(prediction, dim = 1)
    #         pred_idx = probabilities.argmax(dim=1).item()

    #         class_to_index = {v: k for k, v in ImageFolder("dictionaries/letters/train/").class_to_idx.items()}
    #         class_names = class_to_index[pred_idx]
    #         print(class_names)
