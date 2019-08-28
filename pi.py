from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep



class Pi_Control:
	def __init__(self):
		self.__factory = PiGPIOFactory(host="10.0.0.17")
		self.__led = LED(17, pin_factory=self.__factory)
	def on(self):
		self.__led.on()
	def off(self):
		self.__led.off()


