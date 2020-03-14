import eventlet
import socketio
import os
import time

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        client = socketio.Client()

        @client.event
def echo_ack(data):
	t = time.time()
	print([t, 1000.0 * (t - data[0]), 1000.0 * data[1]])
	# sio.emit('echo', [time.time()])


        connected = False
        while not connected:
            try:
            	client.connect('http://localhost:5000')
            	connected = True
            except:
            	connected = False

        while True:
            # print('ON CLIENT')
            client.emit('echo', [time.time()])
            time.sleep(1)
    else:
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
    t = time.time()
    sio.emit('echo_ack', [t, t - data[0]])

@sio.event
def disconnect(sid):
    print('user disconnected', sid)

        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
