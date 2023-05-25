import sys
sys.path.append('.')
import torch
from networks.resnet import create_model

def dataset():
    torch

def main():
    model = create_model(pretrained=False)
    print(model)

if __name__ == '__main__':
    main()

    