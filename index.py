import json
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

payload = ''
orient = {}

while True:
  payload = ser.readline()
  orient = json.loads(payload)
  print(orient)
