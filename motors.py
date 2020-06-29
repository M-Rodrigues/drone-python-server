import RPi.GPIO as GPIO

pinout = {
  'UR': 9, 'UL': 25, 'BR': 11, 'BL': 8
}
F_HZ = 50

class Motors:
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    
    self.p = {}
    for motor in pinout:
      GPIO.setup(pinout[motor], GPIO.OUT)
      self.p[motor] = GPIO.PWM(pinout[motor], F_HZ)
    
  def start(self):
    for motor in pinout:
      self.p[motor].start(50)

  def stop(self):
    for motor in pinout:
      self.p[motor].stop(0)
    GPIO.cleanup()

  def update(self, name, dc):
    self.p[name].ChangeDutyCycle(dc)
