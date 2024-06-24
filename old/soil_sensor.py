from machine import ADC


class SoilSensor:
    def __init__(self, pin_number):
        self.adc = ADC(pin_number)

    def read_moisture_level(self):
        return self.adc.read_u16()  # Returns a value between 0 and 65535
