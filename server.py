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
    sio.emit('echo_ack', [t, t - data[0]], room=sid)

@sio.event
def disconnect(sid):
    print('user disconnected', sid)

@sio.event
def echo_ack(data):
	t = time.time()
	print([t, 1000.0 * (t - data[0]), 1000.0 * data[1]])
	# sio.emit('echo', [time.time()])

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        client = socketio.Client()

        while True:
            print('ON CLIENT')
            client.emit('echo', [time.time()])
            time.sleep(1)
    else:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
