from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time

#initialise serial port S0
serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)

ids = []
#scanning daisy chain and storing ID numbers in array
worked = False
while not worked:
    try:
        ids = serial_connection.scan()
        worked = True
    except:
        pass

#disable torque for servos
for id in ids:
    serial_connection.send(InstructionPacket(id, 0x03, bytes([0x18, 0x00])))

#initialise position array
position = [[None for x in range(0)] for y in range(9)]

start = time.time()
#function that ignores errors when moving
def sure_goto(id, pos, sp):
    max_retries = 10
    retry = 0
    for retry in range(max_retries):
        try:
            serial_connection.goto(id, pos, speed=sp)
            break
        except:
            pass
    print("Retries: {}".format(retry))

try:
    while True:
        for id in ids:
            curr_pos = serial_connection.get_present_position(id)
            position[id].append(curr_pos)
            print(position[id])
            time.sleep(0.04)
            print(time.time()-start)

except KeyboardInterrupt:
    pass

for id in ids:
    sure_goto(id, position[id][0], 200)
    time.sleep(0.08)
    

time.sleep(1)

for i in range(len(position[id])):
    for id in ids:    
        sure_goto(id, position[id][i], 170)
        time.sleep(0.04)
        print(time.time()-start)

serial_connection.close()
print("finished")
