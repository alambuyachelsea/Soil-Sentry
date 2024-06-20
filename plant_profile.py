from water_pump import WaterPump


class PlantProfile:
    def __init__(self, name, water_needs, current_water_level, pump_pin):

        self.name = name
        self.water_needs = water_needs
        self.current_water_level = current_water_level
        self.water_pump = WaterPump(pump_pin)

    def water_plant(self, amount):

        if self.current_water_level < self.water_needs:

            self.water_pump.pump_water(amount / 1000)
            self.current_water_level += amount

            if self.current_water_level > self.water_needs:
                self.current_water_level = self.water_needs

    def get_name(self):
        return self.name

    def get_water_needs(self):
        return self.water_needs

    def get_current_water_level(self):
        return self.current_water_level
