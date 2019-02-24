from pyax12.connection import Connection
import RPi.GPIO as gpio
import time
import os
# Connect to the serial port
#id = 1
serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)

gpio.setwarnings(False)
# Ping the dynamixel unit(s)
ids_available = serial_connection.scan()

for dynamixel_id in ids_available:
    print(dynamixel_id)

# Close the serial connection
serial_connection.close()
