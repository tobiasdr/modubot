from pyax12.connection import Connection
from pyax12.instruction_packet import InstructionPacket
import time
import os
from flask import Flask, render_template
import threading
import rob


app = Flask(__name__)
# serial = None


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/record", methods=['GET'])
def record():
    start = time.time()
    while True:
        for id in ids:
            curr_pos = serial_connection.get_present_position(id)
            position[id].append(curr_pos)
            print(position[id])
            time.sleep(0.08)
            print(time.time()-start)


@app.route("/replay", methods=['GET'])
def replay():
    for id in ids:
        sure_goto(id, position[id][0], 200)
        time.sleep(0.08)
    time.sleep(1)

    for id in ids:
        for i in range(len(position[id])):
            sure_goto(id, position[id][i], 300)
            time.sleep(0.04)
            print(time.time()-start)

if __name__ == "__main__":

    # serial = ...
    t = threading.Thread(target=run)
    t.start()
    app.run(host="0.0.0.0", port=8080)
