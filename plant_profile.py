from water_pump import WaterPump
from soil_sensor import SoilSensor


class PlantProfile:
    def __init__(self, name, water_needs, pump_pin, sensor_pin):
        self.name = name
        self.water_needs = water_needs
        self.water_pump = WaterPump(pump_pin)
        self.soil_sensor = SoilSensor(sensor_pin)

    def water_plant(self, amount):
        self.water_pump.pump_water(amount / 1000) 
        # Assuming 1 second of pump time per 1000ml
        print(f"Watered {self.name} with {amount}ml")

    def get_name(self):
        return self.name

    def get_water_needs(self):
        return self.water_needs

    def get_current_water_level(self):
        return self.soil_sensor.read_moisture_level()
