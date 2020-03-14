import time
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def echo_ack(data):
	t = time.time()
	print([t, 1000.0 * (t - data[0]), 1000.0 * data[1]])
	sio.emit('echo', [time.time()])

@sio.event
def disconnect():
    print('disconnected from server')



sio.connect('http://localhost:5000')
sio.emit('echo', [time.time()])



sio.wait()
