from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time

#initialise serial port S0
serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)

#scanning daisy chain and storing ID numbers in array
ids = serial_connection.scan()

#disable torque for servos
for id in ids:
    serial_connection.send(InstructionPacket(id, 0x03, bytes([0x18, 0x00])))

#initialise position array
position = [[None for x in range(0)] for y in range(len(ids))]
print(position)
#initialise time
start = time.time()

def sure_goto(id, pos, sp):
    max_retries = 10
    retry = 0
    for retry in range(max_retries):
        try:
            serial_connection.goto(id, pos, speed=sp)
            break
        except:
            pass


try:
    while True:
        for id in ids:
            curr_pos = serial_connection.get_present_position(id)
            position[id-1].append(curr_pos)
            print(position[id-1])
            time.sleep(0.05)

except KeyboardInterrupt:
    pass

for id in ids:
    sure_goto(id, position[id-1][0], 200)

time.sleep(1)

for id in ids:
    for i in range(len(position[1])):
        sure_goto(id, position[id-1][i], 200)
        time.sleep(0.08)

print("finished")
