from pyax12.connection import Connection
import time
import os
# Connect to the serial port
serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)

id = 1
serial_connection.goto(id, int(input("Degs?")), speed=512, degrees=True)

id = 2
serial_connection.goto(id, int(input("Degs?")), speed=512, degrees=True)
