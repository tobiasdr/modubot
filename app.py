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
    return render_template('index.html')

@app.route("/record", methods=['GET'])
def record():
    rob.flag = rob.FLAG_RECORD
    return ""


@app.route("/replay", methods=['GET'])
def replay():
    rob.flag = rob.FLAG_REPLAY
    return ""


@app.route("/stop", methods=['GET'])
def stop():
    rob.flag = rob.FLAG_NO_ACTION
    return ""

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

#    print(ids)

    #initialise position array
    position = [[None for x in range(0)] for y in range(9)]
    t = threading.Thread(target=rob.run)
    t.start()
    app.run(host="0.0.0.0", port=8080)
