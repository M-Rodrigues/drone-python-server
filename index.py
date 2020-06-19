import json
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

payload = ''
orient = {}

while True:
  c = ser.read()
  if (c == '\n'):
    orient = json.loads(payload)
    print(orient)
    payload = ''
  else:
    payload += c