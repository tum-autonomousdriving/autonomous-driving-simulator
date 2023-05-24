import socketio
import eventlet
import cv2
#from turbojpeg import TurboJPEG, TJPF_BGR 
import numpy as np

sios = socketio.Server(max_http_buffer_size = 100000000)
app = socketio.WSGIApp(socketio_app=sios)

@sios.event
def connect(sid, environ, auth):
    print('connect ', sid)

#vid = cv2.VideoCapture(0)

@sios.event
def send_frame(sid, data):
    #ret, image = vid.read()
    #success, encoded_image = cv2.imencode('.png', image)
    #image = cv2.resize(image, (4096, 4096))
    #image = TurboJPEG.encode(image)
    #success, image = cv2.imencode('.png', image)
    #cv2.imshow('server',image)
    #cv2.waitKey(1)
    sios.emit(event = 'receive_frame')#, data = image.tobytes())
    print('已发送')

@sios.event
def cs_message(sid, data):
    print(data)
    sios.emit('hi', '你好, C#!')

@sios.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)