# Client-to-Server Server
import socketio
import eventlet

sios = socketio.Server(max_http_buffer_size = 100000000)
app = socketio.WSGIApp(socketio_app=sios)

@sios.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sios.event
def receive_frame(sid, data):
    sios.emit(event = 'send_frame')
    print('received')

@sios.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)