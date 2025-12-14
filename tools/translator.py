"""
Takes pictures of users input and determines string from it
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import timm
from tqdm import tqdm

class CLettersDataset(Dataset):
    """
    Dataset of letters
    """
    def __init__(self, data_dir, transform = None):
        self.__data = ImageFolder(data_dir, transform = transform)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return self.__data[index]

class CSimpleLetterClassifier(nn.Module):
    """
    Class for pytorch model which will clasify users handwritten
    latter into char
    """
    def __init__(self, num_classes = 52):
        super(CSimpleLetterClassifier, self).__init__()

        self.base_model = timm.create_model("efficientnet_b0", pretrained = True)
        self.features = nn.Sequential(*list(self.base_model.children())[:-1])

        enet_out_size = 1280 #efficientnet model base size
        self.classifier = nn.Linear(enet_out_size, num_classes)

    def forward(self, x):
        """
        Defines how will data pass throught network
        """
        x = self.features(x)
        output = self.classifier(x)
        return output


if __name__ == "__main__":
    # Setup Dataset
    transform = transforms.Compose  ([  transforms.Resize((128,128)),
                                        transforms.ToTensor()
                                    ])
    train_foler = "dictionaries/letters/train/"
    valid_foler = "dictionaries/letters/validate/"

    train_dataset = CLettersDataset(train_foler, transform)
    valid_dataset = CLettersDataset(valid_foler, transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle= True)
    valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle= False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    num_epoch = 5
    train_losses = []
    valid_losses = []

    model = CSimpleLetterClassifier(num_classes= 52)
    model.to(device)

    criterion = nn.CrossEntropyLoss()# Loss function
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epoch):
        model.train()
        running_loss = 0.0
        for images, labels in tqdm(train_loader, desc = "Train loop"):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            output = model(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * labels.size(0)
        train_loss = running_loss / len(train_loader.dataset)
        train_losses.append(train_loss)

        # Validation phase
        model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for images, labels in tqdm(valid_loader, desc = "Validation loop"):
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)
                running_loss += loss.item() * labels.size(0)
        valid_loss = running_loss / len(valid_loader.dataset)
        valid_losses.append(valid_loss)

        print(f"Epoch {epoch + 1}/{num_epoch} - Train loss : {train_losses}, Validation loss : {valid_losses}")
