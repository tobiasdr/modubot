from pyax12.connection import Connection
import time

def sure_goto(id, pos):
    max_retries = 10
    retry = 0
    for retry in range(max_retries):
        try:
            serial_connection.goto(id, pos)
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
    new_pos = curr_pos - int(0.12*(curr_load - curr_pos))
    print("Pos: {} Load: {} New pos {}".format(curr_pos, curr_load, new_pos))
    sure_goto(1, new_pos)
    sleep(0.05)
  except:
    pass

sure_goto(1, position1[0])
time.sleep(0.1)
for position in position1:
    sure_goto(1, position)
    time.sleep(0.05)



print('Finished moving')
print('Positions:', position1)

