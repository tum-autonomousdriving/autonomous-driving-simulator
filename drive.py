# simulator_demo.py 中的 data2control 向 drive.py 中的 ai_driver 发送传感器数据，ai_driver 回复控制信号
import socketio
import eventlet
import time
import numpy as np
import torch
from flask import Flask

sios = socketio.Server(max_http_buffer_size = 100000000)
app = Flask(__name__)
app = socketio.WSGIApp(sios, app)
#app = socketio.Middleware(sios, app)

model = torch.load('weights/resnet/0.pt', map_location=torch.device('cpu'))
model.eval()

@sios.event
def connect(sid, environ, auth):
    print('connected ', sid)
    sios.emit(event = 'data2control', data=1)

@sios.on('ai_driver')
def ai_driver(sid, data):

    data = np.frombuffer(data, np.uint8).reshape((480,1920,3)).astype(np.float32)/255
    data = torch.from_numpy(data).permute(2,0,1).unsqueeze(0)

    # output 是三个在(-1,1)区间的浮点数
    output = model(data).detach().numpy()

    sios.emit('data2control', data=output.tobytes())

@sios.event
def disconnect(sid):
    print('disconnect ', sid)
    quit()

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)