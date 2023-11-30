import sys 
sys.path.append('.')

import cv2
import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from collections import OrderedDict
from networks.yolov5_sg import YOLOv5SGModel
from data.cityscapes.labels import trainId2label

if __name__ == '__main__':
    model = YOLOv5SGModel(model_type = 'l')
    for m in model.modules():
        t = type(m)
        if t is nn.Conv2d:
            pass  # nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif t is nn.BatchNorm2d:
            m.eps = 1e-3
            m.momentum = 0.03
        elif t in [nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU]:
            m.inplace = True

    ckpt = torch.load('weights/yolov5_sg/yolov5l_sg.pt', map_location='cpu')

    weights = OrderedDict()

    for name1, name2 in zip(ckpt, model.state_dict()):
        weights[name2] = ckpt[name1]
    
    model.load_state_dict(weights)

    model.eval()

    image = cv2.imread('data/cityscapes/munich_000019_000019_leftImg8bit.png')
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
    image = torch.from_numpy(image).permute(2,0,1).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)[0]
    outputs = F.softmax(outputs, dim=3).cpu().numpy()
    preds = np.argmax(outputs, axis=3)[0]

    h, w = preds.shape
    preds1 = np.zeros((h, w),np.uint8)
    preds2 = np.zeros((h, w, 3),np.uint8)
 
    for j in range(19):
        preds1[preds==j] = trainId2label[j].id
        preds2[preds==j] = trainId2label[j].color
    cv2.imshow('1', preds2[:,:,::-1])
    cv2.waitKey()
