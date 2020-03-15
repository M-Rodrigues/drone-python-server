import eventlet
import socketio
import os
import time

import client

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        client = socketio.Client()

        @client.event
        def echo_ack(data):
            t = time.time()
            print([t, 1000.0 * (t - data[0]), 1000.0 * data[1]])

        connected = False
        while not connected:
            try:
            	client.connect('http://localhost:5000')
            	connected = True
            except:
            	connected = False

        while True:
            client.emit('echo', [time.time()])
            time.sleep(1)
    else:
        client.start()
        