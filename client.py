import socketio
import time
import eventlet

def start():
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
  