from torch import nn
from torchvision import models

def create_model(weights='ResNet50_Weights.DEFAULT'):
    model = models.resnet50(weights = weights)
    model.fc = nn.Sequential(nn.Linear(in_features=2048, out_features=3), nn.Tanh())
    return model

# 测试网络
if __name__ == '__main__':
    model = create_model()
    print(model)