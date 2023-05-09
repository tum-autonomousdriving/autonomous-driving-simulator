import time
import socketio
import cv2
import numpy as np

sioc = socketio.Client()
start_timer = None


def send_ping():
    global start_timer
    start_timer = time.time()
    sioc.emit('send_frame')


@sioc.event
def connect():
    print('connected to server')
    sioc.emit('send_frame')
    #send_ping()

@sioc.event
def receive_frame(data):
    image = np.frombuffer(data, np.uint8).reshape((480,640,3))

    global start_timer
    latency = time.time() - start_timer
    print('latency is {0:.2f} ms'.format(latency * 1000))
    #sioc.sleep(1)
    if sioc.connected:
        send_ping()
        cv2.imshow('client',image)
        cv2.waitKey(30)
        #cv2.imwrite(str(time.time())+'.png', image)

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()