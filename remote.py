import json
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

class AndroidRemote:
  def __init__(self):
    self.ser = ser
  
  def _read_data(self):
    payload = ser.readline()
    return json.loads(payload)
  
  def _send_ack(self):
    ser.write(b'ACK\t')

  def get_data(self ):
    orientation = self._read_data()
    self._send_ack()
    return orientation
  