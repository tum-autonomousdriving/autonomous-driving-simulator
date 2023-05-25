# Server-to-Client Server
import socketio
import eventlet
import time
import numpy as np

sios = socketio.Server(max_http_buffer_size = 100000000)
app = socketio.WSGIApp(socketio_app=sios)

@sios.event
def connect(sid, environ, auth):
    print('connect ', sid)

start = 0

@sios.event
def send_frame(sid):
    global start
    end = time.time() # sent and get response

    if start != 0:
        print('Sending duration', (end-start)*1000,'ms')
    image = np.random.random((2048, 2048, 3))
    start = time.time() # start sending
    sios.emit('receive_frame', data=image.tobytes())


@sios.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)