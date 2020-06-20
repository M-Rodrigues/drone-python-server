import json
import serial

def start_server(q):
  ser = serial.Serial('/dev/rfcomm0', 9600)

  payload = ''
  orient = {}
  
  print('start_server:: Ready')
  while True:
    payload = ser.readline()
    ser.write(b'ACK\t')
    orient = json.loads(payload)
    while not q.empty():
      q.get()
	  q.put(orient)
