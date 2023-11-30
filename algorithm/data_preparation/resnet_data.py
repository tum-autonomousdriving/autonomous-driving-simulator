import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

class SimulatorDataset(Dataset):
    def __init__(self, data_path, phase='train'):
        self.folder_dir = os.path.dirname(data_path)
        f = open(data_path, 'r')
        self.lines = f.readlines()

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        l_img_p, m_img_p, r_img_p, a, b, c = self.lines[idx].strip('\n').split(' ')

        l_img = cv2.imread(os.path.join(self.folder_dir, l_img_p))
        m_img = cv2.imread(os.path.join(self.folder_dir, m_img_p))
        r_img = cv2.imread(os.path.join(self.folder_dir, r_img_p))

        img = np.hstack((l_img, m_img, r_img)).astype(np.float32)/255

        img = torch.from_numpy(img).permute(2,0,1)


        return img, torch.from_numpy(np.array([a, b, c]).astype(np.float32))