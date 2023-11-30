from torch import nn
from torchvision import models

def resnet_model(weights='ResNet50_Weights.DEFAULT'):
    model = models.resnet50(weights = weights)
    model.fc = nn.Sequential(nn.Linear(in_features=2048, out_features=3), nn.Tanh())
    return model

# 测试网络
if __name__ == '__main__':
    model = resnet_model()
    print(model)