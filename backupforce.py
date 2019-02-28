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
wait_time = 0.02
while time.time() - init_time < 6:
  try:
   # start = time.clock_gettime(time.CLOCK_MONOTONIC)
    curr_pos = serial_connection.get_present_position(1)
    position1.append(curr_pos)
    curr_load =  curr_pos + serial_connection.get_present_load(1)
    new_pos = curr_pos - int(0.04*(curr_load - curr_pos))
# - int(0.04 *serial_connection.get_present_speed(1))
    print("Pos: {} Load: {} New pos {} Time {}".format(curr_pos, curr_load, new_pos, (time.time()-init_time)))
    sure_goto(1, new_pos, 400)
   # while time.clock_gettime(time.CLOCK_MONOTONIC) < start+wait_time: 
    #   pass
    time.sleep(0.02)  
  except:
    pass

sure_goto(1, position1[0], 300)
time.sleep(1)
for position in position1:
    sure_goto(1, position, 100)
    print("Time {}".format(time.time()-init_time))
#    while time.clock_gettime(time.CLOCK_MONOTONIC) < start+wait_time: 
 #      pass  
    time.sleep(0.01)

print('Finished moving')
print('Positions:', position1)


