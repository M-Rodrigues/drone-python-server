from math import atan, cos, sin, sqrt
import board
import busio
 
import adafruit_fxos8700
import adafruit_fxas21002c

gyro_offset_x = 0.1323125
gyro_offset_y = 0.2090625
gyro_offset_z = 0.143375

mag_offset_x = 25.93526
mag_offset_y = -30.51872
mag_offset_z = -14.57492

GYRO_ACC_P = 0.95

class IMU:
  def __init__(self):
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.sensor_acc_mag = adafruit_fxos8700.FXOS8700(self.i2c)
    self.sensor_gyro = adafruit_fxas21002c.FXAS21002C(self.i2c)
    
    self.data = {
      'roll': 0, 'pitch': 0, 'yaw': 0
    }

  def get_data(self, dt):
    try:

      acc_x, acc_y, acc_z = self.sensor_acc_mag.accelerometer   # (m/s^2)
      mag_x, mag_y, mag_z = self.sensor_acc_mag.magnetometer    # (uTesla)
      gyro_x, gyro_y, gyro_z = self.sensor_gyro.gyroscope       # (radians/s)
      
      # Calibration offset
      gyro_x -= gyro_offset_x
      gyro_x -= gyro_offset_x
      gyro_x -= gyro_offset_x

      mag_x -= mag_offset_x
      mag_x -= mag_offset_x
      mag_x -= mag_offset_x

      # Normalize
      acc_modulo = sqrt(acc_x ** 2 + acc_y ** 2 + acc_z ** 2)
      mag_modulo = sqrt(mag_x ** 2 + mag_y ** 2 + mag_z ** 2)
      acc_x, acc_y, acc_z = acc_x / acc_modulo, acc_y / acc_modulo, acc_z / acc_modulo
      mag_x, mag_y, mag_z = mag_x / mag_modulo, mag_y / mag_modulo, mag_z / mag_modulo

      # Roll and Pitch from accelerometer
      phi_acc = atan(acc_x / acc_z) 
      theta_acc = atan((-acc_y)/(acc_x*sin(phi_acc) + acc_z*cos(phi_acc))) 

      self.data['roll'] = GYRO_ACC_P * (self.data['roll'] + gyro_y * dt / 1000) + (1 - GYRO_ACC_P) * (phi_acc)
      self.data['pitch'] = GYRO_ACC_P * (self.data['pitch'] + gyro_x * dt / 1000) + (1 - GYRO_ACC_P) * (theta_acc)
      
      # Roll, pitch and yaw from magnetometer
      phi_mag = atan(mag_x / mag_z) 
      theta_mag = atan((-mag_y)/(mag_x*sin(phi_mag) + mag_z*cos(phi_mag))) 
      psi_mag = atan((sin(phi_mag) - cos(phi_mag)) / (cos(theta_mag) + sin(theta_mag)*cos(phi_mag) + sin(theta_mag)*cos(phi_mag)))
      self.data['yaw'] = psi_mag
    except:
      pass

    return self.data
