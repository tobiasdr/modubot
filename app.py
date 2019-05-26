from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time
import os
from flask import Flask, render_template
import threading
import rob


app = Flask(__name__)
# serial = None

flag = 0
@app.route("/")
def main():
    if flag == 1:
        rob.record()
    elif flag == 2:
        rob.replay()
    else:
        pass
    return render_template('index.html')

@app.route("/record", methods=['GET'])
def record():
    flag = 1
    return


@app.route("/replay", methods=['GET'])
def replay():
    flag = 2
    return


if __name__ == "__main__":
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
    position = [[None for x in range(0)] for y in range(12)]
    t = threading.Thread(target=main)
    t.start()
    app.run(host="0.0.0.0", port=8080)
