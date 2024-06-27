import machine
import utime

class UltrasonicSensor:
    def __init__(self, trigger_pin_num, echo_pin_num):
        self.trigger_pin = machine.Pin(trigger_pin_num, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin_num, machine.Pin.IN)

    def read_distance(self):
        # Send a 10us pulse to trigger the sensor
        self.trigger_pin.value(1)
        utime.sleep_us(10)
        self.trigger_pin.value(0)

        # Wait for the echo pin to go high
        while self.echo_pin.value() == 0:
            pulse_start = utime.ticks_us()

        # Wait for the echo pin to go low again
        while self.echo_pin.value() == 1:
            pulse_end = utime.ticks_us()

        # Calculate the duration of the pulse
        pulse_duration = utime.ticks_diff(pulse_end, pulse_start)

        # Speed of sound is approximately 343 meters per second
        # Divide by 2 to account for round trip
        distance = (pulse_duration * 34300) / 2

        # Round the distance to 4 decimal places
        distance_rounded = round(distance, 4)

        return distance_rounded

    def convert_sonic_reading_to_percentage(self, reading):
        # Define the scale thresholds with corresponding percentage values
        thresholds = [
            (3.6015e+07, 0),      # empty reservoir (0%)
            (3.41628e+07, 6), 
            (3.195045e+07, 13),
            (2.92922e+07, 20), 
            (2.74057e+07, 27), 
            (2.46617e+07, 33), 
            (2.31182e+07, 40), 
            (2.148895e+07, 47), 
            (1.97225e+07, 53), 
            (1.733865e+07, 60), 
            (1.534925e+07, 67), 
            (1.31369e+07, 73), 
            (1.15248e+07, 80), 
            (9844100.0, 86), 
            (7443100.0, 93), 
            (4750550.0, 100),     # full reservoir (100%)
        ]

        # Determine the percentage value based on thresholds
        for threshold, percentage in thresholds:
            if reading >= threshold:
                return percentage
        return 100.0  # Default to 100% if below the lowest threshold
