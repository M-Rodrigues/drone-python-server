import time
import multiprocessing
import random
import socketio
import eventlet

def start_drone(q):
	state = 0.0
	while True:
		if not q.empty():
			state = q.get()
			print('State processed at', time.time())
		print('State: {}'.format(state))

def start_server(q):
	random.seed(0)
	while True:
		n = random.randint(1, 10)
		q.put(n)
		print('State received at', time.time())
		time.sleep(random.random() / 10)

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

if __name__ == "__main__": 
	q = multiprocessing.Queue() 

	p1 = multiprocessing.Process(target=start_server, args=(q,)) 
	p2 = multiprocessing.Process(target=start_drone, args=(q,)) 

	p1.start() 
	p2.start() 

	p1.join() 
	p2.join() 
