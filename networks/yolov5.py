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

class Detect(nn.Module):
    # YOLOv5 Detect head for detection models
    #stride = None  # strides computed during build
    dynamic = False  # force grid reconstruction
    export = False  # export mode

    def __init__(self, nc=80, anchors=(), ch=(), inplace=True, stride=None):  # detection layer
        super().__init__()
        self.stride = stride
        self.nc = nc  # number of classes
        self.no = nc + 5  # number of outputs per anchor
        self.nl = len(anchors)  # number of detection layers
        self.na = len(anchors[0]) // 2  # number of anchors
        self.grid = [torch.empty(0) for _ in range(self.nl)]  # init grid
        self.anchor_grid = [torch.empty(0) for _ in range(self.nl)]  # init anchor grid
        self.register_buffer('anchors', torch.tensor(anchors).float().view(self.nl, -1, 2))  # shape(nl,na,2)
        self.m = nn.ModuleList(nn.Conv2d(x, self.no * self.na, 1) for x in ch)  # output conv
        self.inplace = inplace  # use inplace ops (e.g. slice assignment)

    def forward(self, x):
        z = []  # inference output
        for i in range(self.nl):
            x[i] = self.m[i](x[i])  # conv
            bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
            x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()

            if not self.training:  # inference
                if self.dynamic or self.grid[i].shape[2:4] != x[i].shape[2:4]:
                    self.grid[i], self.anchor_grid[i] = self._make_grid(nx, ny, i)

                xy, wh, conf = x[i].sigmoid().split((2, 2, self.nc + 1), 4)
                xy = (xy * 2 + self.grid[i]) * self.stride[i]  # xy
                wh = (wh * 2) ** 2 * self.anchor_grid[i]  # wh
                y = torch.cat((xy, wh, conf), 4)
                z.append(y.view(bs, self.na * nx * ny, self.no))

        return x if self.training else (torch.cat(z, 1),) if self.export else (torch.cat(z, 1), x)
    
    def _make_grid(self, nx=20, ny=20, i=0):
        d = self.anchors[i].device
        t = self.anchors[i].dtype
        shape = 1, self.na, ny, nx, 2  # grid shape
        y, x = torch.arange(ny, device=d, dtype=t), torch.arange(nx, device=d, dtype=t)
        yv, xv = torch.meshgrid(y, x)  # torch>=0.7 compatibility
        grid = torch.stack((xv, yv), 2).expand(shape) - 0.5  # add grid offset, i.e. y = 2.0 * x - 0.5
        anchor_grid = (self.anchors[i] * self.stride[i]).view((1, self.na, 1, 1, 2)).expand(shape)
        return grid, anchor_grid
    
class YOLOv5Model(nn.Module):
    def __init__(self, model_type: 'l', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if model_type=='n':
            ch_n = [16, 32, 64, 128, 256] # channel num
            c3_n = [1, 2, 3]

        if model_type=='s':
            ch_n = [32, 64, 128, 256, 512] # channel num
            c3_n = [1, 2, 3]

        if model_type=='m':
            ch_n = [48, 96, 192, 384, 768] # channel num
            c3_n = [2, 4, 6]

        if model_type=='l':
            ch_n = [64, 128, 256, 512, 1024] # channel num
            c3_n = [3, 6, 9]
        
        if model_type=='x':
            ch_n = [80, 160, 320, 640, 1280] # channel num
            c3_n = [4, 8, 12]

        self.conv_0 = Conv(c1=3, c2=ch_n[0], k=6, s=2, p=2)
        
        self.conv_1 = Conv(c1=ch_n[0], c2=ch_n[1], k=3, s=2)
        self.c3_1 = C3(c1=ch_n[1], c2=ch_n[1], n=c3_n[0])

        self.conv_2 = Conv(c1=ch_n[1], c2=ch_n[2], k=3, s=2)
        self.c3_2 = C3(c1=ch_n[2], c2=ch_n[2], n=c3_n[1])

        self.conv_3 = Conv(c1=ch_n[2], c2=ch_n[3], k=3, s=2)
        self.c3_3 = C3(c1=ch_n[3], c2=ch_n[3], n=c3_n[2])

        self.conv_4 = Conv(c1=ch_n[3], c2=ch_n[4], k=3, s=2)
        self.c3_4 = C3(c1=ch_n[4], c2=ch_n[4], n=c3_n[0])

        self.sppf = SPPF(c1=ch_n[4], c2=ch_n[4], k=5)

        self.conv_5 = Conv(c1=ch_n[4], c2=ch_n[3], k=1, s=1)
        self.c3_5 = C3(c1=ch_n[4], c2=ch_n[3], n=c3_n[0], shortcut=False)

        self.conv_6 = Conv(c1=ch_n[3], c2=ch_n[2], k=1, s=1)
        self.c3_6 = C3(c1=ch_n[3], c2=ch_n[2], n=c3_n[0], shortcut=False)

        self.conv_7 = Conv(c1=ch_n[2], c2=ch_n[2], k=3, s=2)
        self.c3_7 = C3(c1=ch_n[3], c2=ch_n[3], n=c3_n[0], shortcut=False)

        self.conv_8 = Conv(c1=ch_n[3], c2=ch_n[3], k=3, s=2)
        self.c3_8 = C3(c1=ch_n[4], c2=ch_n[4], n=c3_n[0], shortcut=False)

        self.upsample = nn.Upsample(scale_factor=2)
        self.concat = Concat()

        self.detect = Detect(anchors=[[10,13, 16,30, 33,23], [30,61, 62,45, 59,119], [116,90, 156,198, 373,326]], ch=[ch_n[2], ch_n[3], ch_n[4]], stride=[8, 16, 32])

    def forward(self, x):
        # backbone
        x = self.conv_0(x)

        x = self.conv_1(x)
        x = self.c3_1(x)

        x = self.conv_2(x)
        x = self.c3_2(x)

        x_c3_2 = x

        x = self.conv_3(x)
        x = self.c3_3(x)

        x_c3_3 = x

        x = self.conv_4(x)
        x = self.c3_4(x)

        x = self.sppf(x)

        # head
        x = self.conv_5(x)
        x_conv_5 = x
        x = self.upsample(x)
        x = self.concat([x, x_c3_3])
        x = self.c3_5(x)

        x = self.conv_6(x)
        x_conv_6 = x
        x = self.upsample(x)
        x = self.concat([x, x_c3_2])
        x = self.c3_6(x)

        x_c3_6 = x

        x = self.conv_7(x)
        x = self.concat([x, x_conv_6])
        x = self.c3_7(x)

        x_c3_7 = x

        x = self.conv_8(x)
        x = self.concat([x, x_conv_5])
        x = self.c3_8(x)
        
        return self.detect([x_c3_6, x_c3_7, x])
    
if __name__=='__main__':
    model = YOLOv5Model()
    print(model)