# Client-to-Server Client
import time
import socketio
import numpy as np

sioc = socketio.Client()

@sioc.event
def connect():
    print('connected to server')
    sioc.emit(event = 'receive_frame', data='connect')

start = 0

# Send image from client to server.
@sioc.event
def send_frame():
    global start
    end = time.time() # sent and get response

    if start != 0:
        print('Sending duration', (end-start)*1000,'ms')
    image = np.random.random((512, 512, 3))
    if sioc.connected:
        start = time.time() # start sending
        sioc.emit('receive_frame', data=image.tobytes())
        

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()