import eventlet
import socketio
import os
import time

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('a user connected', sid)
    sio.emit('sensor_data_ack', room=sid)

@sio.event
def sensor_data(sid, data):
    sio.emit('sensor_data_ack')

@sio.event
def echo(sid, data):
    print(sid, data)
    t = time.time()
    sio.emit('echo_ack', [t, t - data[0]])

@sio.event
def disconnect(sid):
    print('user disconnected', sid)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        print('HEY')
        time.sleep(1)
        print('HEEEEEEY')
        exit()
    else:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
