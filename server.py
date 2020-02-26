import eventlet
import socketio
from drone import Drone

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
def disconnect(sid):
    print('user disconnected', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet. listen(('', 5000)), app)
