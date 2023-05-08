# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'eventlet'

from flask import Flask, render_template
import socketio
import numpy as np

sios = socketio.Server(async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sios, app.wsgi_app)


@app.route('/')
def index():
    return render_template('latency.html')


@sios.event
def ping_from_client(sid):
    image = np.zeros((100,100,3),np.uint8)
    sios.emit(image, room=sid)


if __name__ == '__main__':
    if sios.async_mode == 'threading':
        # deploy with Werkzeug
        app.run(threaded=True)
    elif sios.async_mode == 'eventlet':
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    elif sios.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        pywsgi.WSGIServer(('', 5000), app).serve_forever()
    elif sios.async_mode == 'gevent_uwsgi':
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
              '--wsgi-file latency.py --callable app')
    else:
        print('Unknown async_mode: ' + sios.async_mode)