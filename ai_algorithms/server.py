import socketio
import eventlet
import cv2

import numpy as np

sio = socketio.Server()
#app = socketio.WSGIApp(sio)
app = socketio.Middleware(sio)

#@sio.event
#def ping_from_client(sid):
#    sio.emit('pong_from_server', room=sid)
#    print('已发送')



@sio.event
def ping_from_client(sid):
    image = cv2.imread('99.jpg')

    #success, encoded_image = cv2.imencode('.png', image)

    sio.emit(event = 'pong_from_server', data = image.tobytes())
    print('已发送Hello world')

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)