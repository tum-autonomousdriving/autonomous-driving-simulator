# Server-to-Client Server
import socketio
import eventlet
import time
import numpy as np
import torch

sios = socketio.Server(max_http_buffer_size = 100000000)
app = socketio.WSGIApp(socketio_app=sios)

model = torch.load('weights/resnet/0.pt', map_location=torch.device('cpu'))
model.eval()

@sios.event
def connect(sid, environ, auth):
    print('connected ', sid)
    sios.emit(event = 'data2control', data='connected')

start = 0

@sios.event
def ai_driver(sid, data):
    data = np.frombuffer(data, np.uint8).reshape((480,640,3)).astype(np.float32)/255
    data = torch.from_numpy(data).permute(2,0,1).unsqueeze(0)
    output = model(data).detach().numpy()

    sios.emit('data2control', data=output.tobytes())

@sios.event
def disconnect(sid):
    print('disconnect ', sid)
    quit()

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)