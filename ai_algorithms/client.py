import time
import socketio

sioc = socketio.Client(logger=True, engineio_logger=True)
start_timer = None


def send_ping():
    global start_timer
    start_timer = time.time()
    sioc.emit('ping_from_client')


@sioc.event
def connect():
    print('connected to server')
    send_ping()


@sioc.event
def pong_from_server():
    global start_timer
    latency = time.time() - start_timer
    print('latency is {0:.2f} ms'.format(latency * 1000))
    sioc.sleep(1)
    if sioc.connected:
        send_ping()


if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()