import threading
from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time
import os
from flask import Flask, render_template

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
            time.sleep(0.3)
        elif flag == FLAG_RECORD:
            record()
        elif flag == FLAG_REPLAY:
            replay()


def record():
    global position
    position = [[None for x in range(0)] for y in range(9)]
    while flag == FLAG_RECORD:
        for id in ids:
            curr_pos = serial_connection.get_present_position(id)
            position[id].append(curr_pos)
            print(position[id])
            time.sleep(0.08)
            print(time.time()-start) 


def replay():
    global position
    move_counter = 0
    for id in ids:
        sure_goto(id, position[id][0], 200)
        time.sleep(0.08)
    time.sleep(1)

    while flag == FLAG_REPLAY and move_counter < len(position[ids[0]]):
        for id in ids:
            for i in range(len(position[id])):
                sure_goto(id, position[id][i], 300)
                time.sleep(0.04)
                print(time.time()-start)   
                move_counter += 1
  
