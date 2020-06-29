import time

from remote import AndroidRemote
from motors import Motors
from imu import IMU
from pid import PID

remote_ctl = AndroidRemote()
drone_motors = Motors()
drone_imu = IMU()
pid = PID()

print('start_server:: Ready!')
drone_motors.start()
print('start_motors:: Ok!')

# power = 0
power = {
  'UR': 30, 'UL': 30, 'BR': 30, 'BL': 30
}

t1 = time.time()
try:
  while True:
    # Get data from android orientation
    target_state = remote_ctl.get_data()

    # Get data from local sensor
    t2 = time.time()
    cur_state = drone_imu.get_data(t2 - t1)
    
    # Find difference between actual and target values.
    error_state = {}
    for direction in cur_state:
      error_state[direction] = cur_state[direction] - target_state[direction]

    # Calculate needed corrections (PID)
    corrections = pid.update(error_state, t2 - t1)

    # Apply corrections to motors
    for motor_key in power:
      # power[motor_key] = (power[motor_key] + 10) % 100
      motor_power = power[motor_key] + corrections[motor_key] * 300
      motor_power = min(100, max(0, motor_power))
      drone_motors.update(motor_key, motor_power)


    print('cur_state\t', cur_state)
    # print('target_state\t', target_state)
    # print('error_state\t', error_state)
    # print('power\t\t', power)
    # print('corrections\t', corrections)
    print('\n')

    t1 = t2
except KeyboardInterrupt:
  pass

drone_motors.stop()
print('stop_motors:: Ok!')
