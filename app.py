import time
import multiprocessing
import random
import socketio
import eventlet

def start_drone(q):
	while True:
		if not q.empty():
			state = q.get()
			print('Orientation state updated', state)

def start_server(q):
	sio = socketio.Server(cors_allowed_origins='*')
	app = socketio.WSGIApp(sio)

	@sio.event
	def connect(sid, environ):
		print('a user connected', sid)
		sio.emit('connected', room=sid)

	@sio.event
	def sensor_data(sid, data):
		if not q.empty():
			q.get()
		q.put(data)
		sio.emit('sensor_data_ack')

	@sio.event
	def echo(sid, data):
		sio.emit('echo_ack', data)

	@sio.event
	def disconnect(sid):
		print('user disconnected', sid)

	eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

if __name__ == "__main__": 
	q = multiprocessing.Queue() 

	p1 = multiprocessing.Process(target=start_server, args=(q,)) 
	p2 = multiprocessing.Process(target=start_drone, args=(q,)) 

	p1.start() 
	p2.start() 

	p1.join() 
	p2.join() 
