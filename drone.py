class Motor:
  def __init__(self):
    pass
  

class Drone:
  def __init__(self):
    self.motor = {
      'FR': Motor(), 'FL': Motor(),
      'BR': Motor(), 'BL': Motor(),
    }
    print('Drone Criado')
