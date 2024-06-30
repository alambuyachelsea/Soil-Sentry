from machine import Pin
import time


class WaterPump:
    def __init__(self, pin_number):
        self.pump = Pin(pin_number, Pin.OUT)
        self.pump.value(0)  # Ensure the pump is off initially

    def turn_on(self):
        self.pump.value(1)
        print(f"Water pump on pin {self.pump} is ON")

    def turn_off(self):
        self.pump.value(0)
        print(f"Water pump on pin {self.pump} is OFF")

    def pump_water(self, duration=10):
        self.turn_on()
        time.sleep(duration)
        self.turn_off()
