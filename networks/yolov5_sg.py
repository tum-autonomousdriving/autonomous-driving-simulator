import torch
from torch import nn
import warnings

class Concat(nn.Module):
    # Concatenate a list of tensors along dimension
    def __init__(self, dimension=1):
        super().__init__()
        self.d = dimension

    def forward(self, x):
        return torch.cat(x, self.d)
    
def autopad(k, p=None, d=1):  # kernel, padding, dilation
    # Pad to 'same' shape outputs
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p

class Conv(nn.Module):
    # Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)
    default_act = nn.SiLU(True)  # default activation

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        super().__init__()
        self.conv = nn.Conv2d(c1, c2, k, s, autopad(k, p, d), groups=g, dilation=d, bias=False)
        self.bn = nn.BatchNorm2d(c2, 1e-3, 0.03)
        self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

    def forward_fuse(self, x):
        return self.act(self.conv(x))

class Bottleneck(nn.Module):
    # Standard bottleneck
    def __init__(self, c1, c2, shortcut=True, g=1, e=0.5):  # ch_in, ch_out, shortcut, groups, expansion
        super().__init__()
        c_ = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, c_, 1, 1)
        self.cv2 = Conv(c_, c2, 3, 1, g=g)
        self.add = shortcut and c1 == c2

    def forward(self, x):
        return x + self.cv2(self.cv1(x)) if self.add else self.cv2(self.cv1(x))
    
class C3(nn.Module):
    # CSP Bottleneck with 3 convolutions
    def __init__(self, c1, c2, n=1, shortcut=True, g=1, e=0.5):  # ch_in, ch_out, number, shortcut, groups, expansion
        super().__init__()
        c_ = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, c_, 1, 1)
        self.cv2 = Conv(c1, c_, 1, 1)
        self.cv3 = Conv(2 * c_, c2, 1)  # optional act=FReLU(c2)
        self.m = nn.Sequential(*(Bottleneck(c_, c_, shortcut, g, e=1.0) for _ in range(n)))

    def forward(self, x):
        return self.cv3(torch.cat((self.m(self.cv1(x)), self.cv2(x)), 1))

class SPPF(nn.Module):
    # Spatial Pyramid Pooling - Fast (SPPF) layer for YOLOv5 by Glenn Jocher
    def __init__(self, c1, c2, k=5):  # equivalent to SPP(k=(5, 9, 13))
        super().__init__()
        c_ = c1 // 2  # hidden channels
        self.cv1 = Conv(c1, c_, 1, 1)
        self.cv2 = Conv(c_ * 4, c2, 1, 1)
        self.m = nn.MaxPool2d(kernel_size=k, stride=1, padding=k // 2)

    def forward(self, x):
        x = self.cv1(x)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')  # suppress torch 1.9.0 max_pool2d() warning
            y1 = self.m(x)
            y2 = self.m(y1)
            return self.cv2(torch.cat((x, y1, y2, self.m(y2)), 1))

class Segment(nn.Module):
    # YOLOv5 Detect head for detection models
    #stride = None  # strides computed during build
    dynamic = False  # force grid reconstruction
    export = False  # export mode

    def __init__(self, nc=80, ch=(), inplace=True, stride=None):  # detection layer
        super().__init__()
        self.stride = stride
        self.nc = nc  # number of classes
        self.nl = len(ch)  # number of detection layers
        self.m = nn.ModuleList(nn.Conv2d(x, self.nc, 1) for x in ch)  # output conv
        self.inplace = inplace  # use inplace ops (e.g. slice assignment)

    def forward(self, x):
        for i in range(self.nl):
            x[i] = self.m[i](x[i])  # conv
            x[i] = x[i].permute(0, 2, 3, 1).contiguous()

        return x
    
class YOLOv5SGModel(nn.Module):
    def __init__(self, model_type = 'l', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if model_type=='n':
            ch = [16, 32, 64, 128, 256] # channel num
            c3_n = [1, 2, 3]

        if model_type=='s':
            ch = [32, 64, 128, 256, 512] # channel num
            c3_n = [1, 2, 3]

        if model_type=='m':
            ch = [48, 96, 192, 384, 768] # channel num
            c3_n = [2, 4, 6]

        if model_type=='l':
            ch = [64, 128, 256, 512, 1024] # channel num
            c3_n = [3, 6, 9]
        
        if model_type=='x':
            ch = [80, 160, 320, 640, 1280] # channel num
            c3_n = [4, 8, 12]

        self.conv_0 = Conv(c1=3, c2=ch[0], k=6, s=2, p=2)   # 0
        
        self.conv_1 = Conv(c1=ch[0], c2=ch[1], k=3, s=2)    # 1
        self.c3_1 = C3(c1=ch[1], c2=ch[1], n=c3_n[0])   # 2

        self.conv_2 = Conv(c1=ch[1], c2=ch[2], k=3, s=2)    # 3
        self.c3_2 = C3(c1=ch[2], c2=ch[2], n=c3_n[1])   # 4

        self.conv_3 = Conv(c1=ch[2], c2=ch[3], k=3, s=2)    # 5
        self.c3_3 = C3(c1=ch[3], c2=ch[3], n=c3_n[2])   # 6

        self.conv_4 = Conv(c1=ch[3], c2=ch[4], k=3, s=2)    # 7
        self.c3_4 = C3(c1=ch[4], c2=ch[4], n=c3_n[0])   # 8

        self.sppf = SPPF(c1=ch[4], c2=ch[4], k=5)   # 9

        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear') # 11 15
        self.upsample_x4 = nn.Upsample(scale_factor=4, mode='bilinear')
        self.concat = Concat()  # 12 16 19 22

        self.conv_5 = Conv(c1=ch[4], c2=ch[3], k=1, s=1)    # 10
        self.c3_5 = C3(c1=ch[3]+ch[3], c2=ch[3], n=c3_n[0], shortcut=False)   # 13

        self.conv_6 = Conv(c1=ch[3], c2=ch[2], k=1, s=1)    # 14
        self.c3_6 = C3(c1=ch[2]+ch[2], c2=ch[2], n=c3_n[0], shortcut=False)   # 17

        self.conv_7 = Conv(c1=ch[2], c2=ch[1], k=1, s=1)    # 18
        self.c3_7 = C3(c1=ch[1]+ch[1], c2=ch[1], n=c3_n[0], shortcut=False)   # 20

        self.conv_8 = Conv(c1=ch[1], c2=ch[1], k=1, s=1)    # 21

        self.detect = Segment(nc=19, ch=[ch[1]], stride=[8, 16, 32])

    def forward(self, x):
        # backbone
        x = self.conv_0(x)

        x = self.conv_1(x)
        x = self.c3_1(x)

        x_2 = x

        x = self.conv_2(x)
        x = self.c3_2(x)

        x_4 = x

        x = self.conv_3(x)
        x = self.c3_3(x)

        x_6 = x

        x = self.conv_4(x)
        x = self.c3_4(x)

        x = self.sppf(x)

        # head
        x = self.conv_5(x)
        x = self.upsample(x)
        x = self.concat([x, x_6])
        x = self.c3_5(x)

        x = self.conv_6(x)
        x = self.upsample(x)
        x = self.concat([x, x_4])
        x = self.c3_6(x)

        x = self.conv_7(x)
        x = self.upsample(x)
        x = self.concat([x, x_2])
        x = self.c3_7(x)

        x = self.conv_8(x)
        x = self.upsample_x4(x)
        
        return self.detect([x])
    
if __name__=='__main__':
    model = YOLOv5SGModel()
    x = torch.rand((1,3,640,640))
    x = model(x)
    print(model)