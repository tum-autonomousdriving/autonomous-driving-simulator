import os
from torch.utils.data import Dataset

class sim_dataset(Dataset):
    def __init__(self, data_path, phase='train'):

        file_paths = os.listdir(data_path)
        
        if phase == 'train':
            print(data_path)
        if phase == 'val':
            print(data_path)
        if phase == 'test':
            print('test')
        self
        
    def __len__(self):
        return

    def __getitem__(self, idx):
        return