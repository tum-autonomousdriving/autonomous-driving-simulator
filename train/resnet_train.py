import sys
sys.path.append('.')

import os
import argparse

import torch
from networks.resnet import create_model
from torch.utils.data import DataLoader
from data_processing.simulator import simulator_dataset


def train_val():
    # 第一步：构建数据读取迭代器

    train_data = simulator_dataset(data_path = os.path.join(cfg.data_path, 'train'), phase='train')
    val_data = simulator_dataset(data_path = os.path.join(cfg.data_path, 'val'), phase='val')

    train_dataloader = DataLoader(train_data, batch_size=cfg.batch_size, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=cfg.batch_size*2, shuffle=False)

    # 第二步：设置训练参数：学习率、学习率衰减策略、优化函数（SDG、Adam、……）、损失函数、……

    optimizer = torch.optim.SGD(lr=cfg.learning_rate)

    loss_function = torch.nn.MSELoss()

    # 第三步： 初始化网络，循环读取数据训练网络

    if cfg.device == 'cpu':
        device = torch.device('cpu')
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = cfg.device
        device = torch.device('gpu:0')

    model = create_model(pretrained=False).to(device=device)
    for epoch in range(cfg.epochs):
        model.train()

        for input, target in train_dataloader:
            input, target = input.to(cfg.device), target.to(cfg.device)
            output = model(input)
            loss = loss_function(output, target)

        # 训练完每个epoch进行验证
        model.eval()
        with torch.no_grad():
            for input, target in val_dataloader:
                input, target = input.to(cfg.device), target.to(cfg.device)
                output = model(input)
                loss = loss_function(output, target)

        torch.save()
        torch.cuda.empty_cache()

def parse_cfg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=100, help='total number of training epochs')
    parser.add_argument('--data-path', type=str, default='data/simulator', help='data path')
    parser.add_argument('--device', type=str, default='0', help='e.g. cpu or 0 or 0,1,2,3')
    parser.add_argument('--batch-size', type=int, default=64, help='batch size')
    parser.add_argument('--learning-rate', type=int, default=0.01, help='initial learning rate')

    return parser.parse_args()

if __name__ == '__main__':
    cfg = parse_cfg()
    
    train_val(cfg)

    