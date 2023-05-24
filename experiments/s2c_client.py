# Server-to-Client Client
import socketio

sioc = socketio.Client()

@sioc.event
def connect():
    print('connected to server')
    sioc.emit(event = 'send_frame')

start = 0

# Send image from client to server.
@sioc.event
def receive_frame(data):
    sioc.emit(event = 'send_frame')
    print('received')
        

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()