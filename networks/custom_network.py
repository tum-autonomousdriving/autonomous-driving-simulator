from torch import nn

class custom_model(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conv0 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3,stride=1,padding=1)

    def forward(self, x):
        x = self.conv0(x)
        return x
    
# 测试网络
if __name__ == '__main__':
    model = custom_model()
    print(model)