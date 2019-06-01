import threading
from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time
import os


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


FLAG_NO_ACTION = 0
FLAG_RECORD = 1
FLAG_REPLAY = 2

flag = FLAG_NO_ACTION
position = [[None for x in range(0)] for y in range(9)]

def run():
    while 1:
        if flag == FLAG_NO_ACTION:
            #disable torque for servos
            for id in ids:
                serial_connection.send(InstructionPacket(id, 0x03, bytes([0x18, 0x00])))          
        elif flag == FLAG_RECORD:
            record()
        elif flag == FLAG_REPLAY:
            replay()


def record():
    global position
    position = [[None for x in range(0)] for y in range(9)]
    while flag == 1:
        for id in ids:
            curr_pos = serial_connection.get_present_position(id)
            position[id].append(curr_pos)
            print(position[id])
            time.sleep(0.08)
    

def replay():
    global position
    for id in ids:
        sure_goto(id, position[id][0],50)
        time.sleep(0.08)
    time.sleep(1)

    for i in range(len(position[id])):
        for id in ids:
            sure_goto(id, position[id][i], 50)
            time.sleep(0.08)
  
