Kp_roll = 1.0
Ki_roll = 1.0
Kd_roll = 1.0

Kp_pitch = 1.0
Ki_pitch = 1.0
Kd_pitch = 1.0

class PID:
  def __init__(self):
    self.prev_errors = { 'roll': 0, 'pitch': 0, 'yaw': 0 }
    self.IError_roll, self.DError_roll = 0, 0
    self.IError_pitch, self.DError_pitch = 0, 0

  def update(self, errors, dt):
    updates = {
      'UR': 0, 'UL': 0, 'BR': 0, 'BL': 0
    }

    # Roll PID - front/back compensation
    self.IError_roll += errors['roll'] * dt
    self.DError_roll = (errors['roll'] - self.prev_errors['roll']) / dt
    
    d_roll = Kp_roll * errors['roll'] + Ki_roll * self.IError_roll + Kd_roll * self.DError_roll
    
    updates['UR'] -= (d_roll / 2)
    updates['UL'] -= (d_roll / 2)
    updates['BR'] += (d_roll / 2)
    updates['BL'] += (d_roll / 2)

    # Pitch PID - left/right compensation
    self.IError_pitch += errors['pitch'] * dt
    self.DError_pitch = (errors['pitch'] - self.prev_errors['pitch']) / dt
    
    d_pitch = Kp_pitch * errors['pitch'] + Ki_pitch * self.IError_pitch + Kd_pitch * self.DError_pitch
    
    updates['UR'] -= (d_pitch / 2)
    updates['BR'] -= (d_pitch / 2)
    updates['UL'] += (d_pitch / 2)
    updates['BL'] += (d_pitch / 2)

    self.prev_errors = errors
    return updates