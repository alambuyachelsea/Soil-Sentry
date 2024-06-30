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
        reading = self.soil_sensor.read_moisture_level()
        level = self.convert_soil_moisture_to_scale(reading)

        return level

    def convert_soil_moisture_to_scale(reading):
        # Define the scale thresholds
        thresholds = [
            (24093.30, 1),  # air in a closed room
            (21060.00, 2),  # very dry soil
            (17684.50, 3),  # lightly watered soil
            (13991.00, 4),  # heavily watered soil
            (13613.18, 5)   # 100% water
        ]

        # Determine the scale value based on thresholds
        for threshold, scale_value in thresholds:
            if reading >= threshold:
                return scale_value
        return 5  # Default to 5 if below the lowest threshold
