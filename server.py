import socketio
import eventlet

def start_server(q):
	sio = socketio.Server(cors_allowed_origins='*')
	app = socketio.WSGIApp(sio)

	@sio.event
	def connect(sid, environ):
		print('a user connected', sid)
		sio.emit('connected', room=sid)
		sio.emit('sensor_data_ack', room=sid)

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