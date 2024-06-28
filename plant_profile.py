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
        return self.soil_sensor.measure_current_water_level()

    def get_img_source(self):
        return self.img_source
