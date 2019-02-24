from pyax12.connection import Connection
import time
import keyboard

serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)
position1 = []
run = True
init_time = time.time()
print(init_time)
while time.time() - init_time < 10:
  try:
    start_time = time.time()
    curr_pos = serial_connection.get_present_position(1)
    position1.append(curr_pos)
    curr_load =  curr_pos+serial_connection.get_present_load(1)
    new_pos = curr_pos-int(0.08*(curr_load-curr_pos))
    serial_connection.goto(1, new_pos)
    print("Recording\tPos: {} Load: {} New pos {}\t'Time taken:{}".format(curr_pos, curr_load, new_pos, start_time - time.time()))
    time.sleep(0.1)
  except Exception as e:
    print(e)
    pass
#  if keyboard.is_pressed('q'):
#      run = False


print('Finished recording')
print('Positions:', position1)

