![Alt text](assets/dashboard.png)

## Table of contents
- [Table of content](#table-of-contents)
- [Author](#author)
- [Project Overview](#project-overview)
- [Estimated time](#estimated-time)
- [Project Objective](#project-objective)
- [Materials](#bill-of-materials)
- [Computer setup](#computer-setup)
  - [Preparing the development environment](#preparing-the-development-environment)
  - [Preparing the Pico W for Micropython (More info here)](#preparing-the-pico-w-for-micropython-more-info-here)
  - [Uploading the code onto the Pico W](#uploading-the-code-onto-the-pico-w)
- [Putting everything together](#putting-everything-together)
- [Platform](#platform)
  - [Beginner: Adafruit](#beginner-adafruit)
  - [More Advanced: TIG stack](#more-advanced-tig-stack)
- [The code](#the-code)
  - [Class Diagram](#class-diagram)
  - [AnalogSensor class](#analogsensor-class)
  - [WiFiConnector class](#wificonnector-class)
  - [MQTTclient class](#mqttclient-class)
  - [my\_secrets](#my_secrets)
  - [boot and main](#boot-and-main)
  - [Unit testing](#unit-testing)
- [Transmitting the data / connectivity](#transmitting-the-data--connectivity)
  - [Deployment diagram](#deployment-diagram)
  - [Data's journey](#datas-journey)
  - [Protocols](#protocols)
- [Presenting the data](#presenting-the-data)
- [Finalizing the design](#finalizing-the-design)


## Author
By Alambuya Chelsea CA223SF

## Project Overview
The soil sentry is a small scale irrigation system which allows a user to connect multiple plants with various water consumption needs, monitor their water levels and supply water them when needed in addition to monitoring the water reservoir levels. 

## Estimated Time
- Is the amount of time for the project estimated??? meaning what

## Project Objective
Many at home watering solutins exist but are limited to just soil moisture levels and water supply. These solutions are sufficient for plants that have the same water consumption needs but to an owner of various plant types like succulents, herbs and flowering plants this can lead to over or under watering plants by trying to calibrate a single water supply to them.
With the soil sentry, a user can create differnt plant profiles where each plant's water consumption needs will determine how offen it recieves water from the supply. Additionally, the water reservoir is monitored which allows the user to know when re-fill it.
By monitoring the data, users can have a better idea of their plant needs, reduce water waste by ensuring the plants are only watered when they need it.

## Bill of Materials
These items can be purchased online at stores that sells electronic components, single board computers, modules, sensors etc. Reliable options are [The pi hut](thepihut.com), [electrokit](electrokit.com), [amazon.se](amazon.se) and any non electronic components can be found at a hardware store.
| Component|Price (SEK)|Purpose|
|---|---|---|
| Raspberry Pi Pico W| 89| Reads the sensor data and transmits it to the server|
| Capacitive Soil Moisture Sensor *| 44| To measure the soil moisture level |
| Submersible waterpump 3V *| 45| To pump the water from the reservoir to the plants|
| 5V Relay Module *| 60| Handles switching operations between the 3V pump and a separate 5V control signal|
| 9V Battery| 60| Power Supply for the water  pumps|
| HC-SR04 Ultrasonic Range Sensor| 23| To measure the reservoir level|
| Male/Male Jumper Wires & Female/Male Jumper Wires| 100| To connect components to the Pico|
| Silicon Water Pipe| 45| To transport water to the plant|
| 2 Core Electric Cable| 121| To extend the length of jumper wires|
| Soldering Iron Kit| 500| To join 2 wires|
| Soldering Wire| 100| To join 2 wires|
| Desoldering Wick| 100| To erase the makes you made (with the soldering, not in real life)|
| Electric Tape| 60| To seal soldered wires that will be placed in water|
| Heat Shrink| 90| To seal soldered wires that will be placed in water|

  * Get one per plant you intend to monitor

## Computer Setup
### IDE
I developed this on a computer running windows 11. I decided to use Thonny for the microcontroller code because it is specifically designed for beginners in MicroPython programming, offering an intuitive interface, easy debugging tools for microcontroller projects. Installation instruction can be found on the [Thonny website](https://thonny.org/). For the server side code I used VS Code

### Raspberry Pi Pico W setup
To set up the pico first download the latest version of Raspberry Pi Pico W firmware [here](https://rpf.io/pico-w-firmware), once downloaded connect the pico to your computer while holding down the bootsel button. A file manager should open with the raspberry pi pico w as the connected device, copy the firmware file to the device and the file manager will close. Open the Thonny editor and on the navigation bar, select Tools > Options > Interpreter and choose the MicroPython interpreter for Raspberry Pi Pico.

### Wiring
![Alt text](assets/Circuit_diagram/circuit_diagram.png)

- Breadboard - I connected 2 boards to reduce crowding but it's possible to have everything on one.

- Raspberry Pi Pico W - place the Pico over the center of the breadboard with the pins straddling the center divide. Connect the pico's GND to the (-) line on the right side of the breadboard and the 3V3 output to the (+) line on the on the right side of the breadboard. See the attached pico w pinout for guidance. 
![Alt text](assets/picow-pinout.png)

- 9V Battery - Connect the battery's (-) to the (-) and the (+) to the (+) lines on the left side of the breadboard.

- Soil moisture sensors - For my set up, I used analog sensors so I was limited to 3 analog to digital converter (ADC) pins on the pico i.e. GP26, GP27 and GP28. This will be placed in the soil to measure the moisture content. Connect the sensor's vcc to the (+) line on the bread board, the GND to the (-) line on the breadboard and the analog output to one of the ADC pins. Since soil sensors are different you may have to calibrate them according to your environment. Follow these steps to calibrate them;

  - Take readings in open air, very dry soil, dry soil, lightly watered soil, heavily watered soil and 100% water. 
  - Take about 100 readings for each find the highest and lowest values
  - Create a scale of 0 - 5 where 0 is open air and 5 is 100% water.

- Ultra sonic sensor - This should rest on top of the water reservoir. For this project, I designed a 3D mount to set on top of the reservoir. Connect the sensor's GND to any (-)line on the breadboard and the vcc to any (+) line on the breadboard. Connect the trig pin to GPIO 0 and connect the echo pin to GPIO 1.
![Alt text](assets/reservoir_mount.jpg)
Calibrating the ultra sonic sensor is similar to the soil moisture sensors;
  - Set up the sensor above the reservoir and take readings when the reservoir is empty, and slowly increase the water level taking several readings as you go.
  - Create a percentage scale after getting the reading at multiple levels.

- Water Pump and 5V relay module - Connect the water pump's gnd to the left side (-) line on the breadboard and the the pump's (+) line to the relays normally open(NO) terminal. Then connect the relay's (-) and (+) pins to the GND and the (+) line on the left side of the breadboard. Connect the relays control input pin to any available GPIO pin.

### 
Upload the the main.py, plant_profile.py, water_pump.py, ultrasonic_sensor.py and soil_sensor.py files to the pico

### Platform
