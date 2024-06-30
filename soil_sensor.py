from machine import ADC


class SoilSensor:
    def __init__(self, pin_number):
        self.adc = ADC(pin_number)

    def read_moisture_level(self):
        return self.adc.read_u16()  # Returns a value between 0 and 65535

    def measure_current_water_level(self):
        reading = self.read_moisture_level()
        level = self.convert_soil_moisture_to_scale(reading)
        return level

    def convert_soil_moisture_to_scale(self, reading):
        thresholds = [
            (24293, 0),  # Air in a dry room
            (24093, 1),  # Extremely dry soil
            (21060, 2),  # Dry soil
            (17684, 3),  # lightly watered soil
            (15991, 4),  # heavily watered soil
            (13713, 5)   # 100% water
        ]

        for threshold, scale_value in thresholds:
            if reading >= threshold:
                return scale_value
        return 5  # Default to 5 if below the lowest threshold
