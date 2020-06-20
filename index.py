import json
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

payload = ''
orient = {}

print('Ready')
while True:
  payload = ser.readline()
  # print(payload)
  orient = json.loads(payload)
  print(orient)
  ser.write(b'ACK\t')
