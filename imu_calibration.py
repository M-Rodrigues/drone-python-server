import time
import board
import busio
from statistics import mean, stdev
 
import adafruit_fxos8700
import adafruit_fxas21002c

# The values for offset aftee this calibration were
#
# Gyroscope offset: (mean, std)
# X: 0.1323125  0.18466651785466298
# Y: 0.2090625  0.14371279766242798
# Z: 0.143375   0.1347482057541174
#
# Magnetometer offset:
# X: 25.93526 7.08914
# Y: -30.51872 12.36429
# Z: -14.57492 10.45313

i2c = busio.I2C(board.SCL, board.SDA)
sensor_acc_mag = adafruit_fxos8700.FXOS8700(i2c)
sensor_gyro = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=2000)

T, dt = 10, 0.01

gyro_x_data = []
gyro_y_data = []
gyro_z_data = []

mag_x_data = []
mag_y_data = []
mag_z_data = []

k = 0
for i in range(int(T/dt)):
  mag_x, mag_y, mag_z = sensor_acc_mag.magnetometer    # (uTesla)
  gyro_x, gyro_y, gyro_z = sensor_gyro.gyroscope       # (radians/s)

  gyro_x_data.append(gyro_x - gyro_offset_x)
  gyro_y_data.append(gyro_y - gyro_offset_y)
  gyro_z_data.append(gyro_z - gyro_offset_z)

  mag_x_data.append(mag_x - mag_offset_x)
  mag_y_data.append(mag_y - mag_offset_y)
  mag_z_data.append(mag_z - mag_offset_z)

  time.sleep(dt)
  
  if k == 0:
    print('t: {} of {}'.format(i*dt, T))
  k = (k + 1) % int(1/dt)

print('Gyroscope offset: \nX: {} {}\nY: {} {}\nZ: {} {}'.format(
  mean(gyro_x_data), 
  stdev(gyro_x_data), 
  mean(gyro_y_data), 
  stdev(gyro_y_data), 
  mean(gyro_z_data),
  stdev(gyro_z_data))
  )
print('\n')  
print('Magnetometer offset: \nX: {} {}\nY: {} {}\nZ: {} {}'.format(
  mean(mag_x_data), 
  stdev(mag_x_data), 
  mean(mag_y_data), 
  stdev(mag_y_data), 
  mean(mag_z_data),
  stdev(mag_z_data))
  )
