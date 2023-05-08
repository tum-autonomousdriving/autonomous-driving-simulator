import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)

app = socketio.WSGIApp(sio)



@sio.event
def ping_from_client(sid):
    sio.emit('pong_from_server', room=sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)