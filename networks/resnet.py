from torch import nn
from torchvision import models

def create_model(weights='ResNet50_Weights.DEFAULT'):
    model = models.resnet50(weights = weights)
    model.fc = nn.Linear(in_features=2048, out_features=3)
    return model

if __name__ == '__main__':
    model = create_model()
    print(model)