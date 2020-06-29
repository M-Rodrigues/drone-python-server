class PID:
  def __init__(self):
    pass

  def update(self, errors):
    updates = {
      'UR': 0, 'UL': 0, 'BR': 0, 'BL': 0
    }

    # Roll PID - front/back compensation
    d_roll = errors['roll']
    updates['UR'] -= (d_roll / 2)
    updates['UL'] -= (d_roll / 2)
    updates['BR'] += (d_roll / 2)
    updates['BL'] += (d_roll / 2)

    # Pitch PID - left/right compensation
    d_pitch = errors['pitch']
    updates['UR'] -= (d_pitch / 2)
    updates['BR'] -= (d_pitch / 2)
    updates['UL'] += (d_pitch / 2)
    updates['BL'] += (d_pitch / 2)

    return updates