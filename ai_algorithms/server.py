import socketio
import eventlet
import cv2

import numpy as np

sios = socketio.Server()
#app = socketio.WSGIApp(sio)
app = socketio.Middleware(sios)

vid = cv2.VideoCapture(0)

@sios.event
def send_frame(sid):
    ret, image = vid.read()
    #success, encoded_image = cv2.imencode('.png', image)
    cv2.imshow('server',image)
    cv2.waitKey(1)
    sios.emit(event = 'receive_frame', data = image.tobytes())
    print('已发送')

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)