from pyax12.connection import Connection
import time

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

serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)
position1 = []
init_time = time.time()
while time.time() - init_time < 6:
  try:
    # start_time = time.time()
    curr_pos = serial_connection.get_present_position(1)
    position1.append(curr_pos)
    curr_load =  curr_pos + serial_connection.get_present_load(1)
    new_pos = curr_pos - int(0.04*(curr_load - curr_pos))
# - int(0.01 *(250 - serial_connection.get_present_speed(1)))
    print("Pos: {} Load: {} New pos {}".format(curr_pos, curr_load, new_pos))
    sure_goto(1, new_pos, 600)
    sleep(0.01)
  except:
    pass

sure_goto(1, position1[0], 300)
time.sleep(0.1)
for position in position1:
    sure_goto(1, position, 750)
    time.sleep(0.08)



print('Finished moving')
print('Positions:', position1)


