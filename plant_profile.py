from water_pump import WaterPump
from soil_sensor import SoilSensor


class PlantProfile:
    def __init__(self, name, water_needs, pump_pin, sensor_pin, img_source):
        self.name = name
        self.water_needs = water_needs
        self.pump_pin = pump_pin
        self.sensor_pin = sensor_pin
        self.soil_sensor = SoilSensor(sensor_pin)
        self.img_source = img_source

    def get_name(self):
        return self.name

    def get_water_needs(self):
        return self.water_needs

    def get_current_water_level(self):
        reading = self.soil_sensor.read_moisture_level()
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

    def get_img_source(self):
        return self.img_source
