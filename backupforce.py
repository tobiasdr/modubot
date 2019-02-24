
from pyax12.connection import Connection

serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000, rpi_gpio=True)

while 1:
  try:
    curr_pos = serial_connection.get_present_position(1)
    curr_load =  curr_pos+serial_connection.get_present_load(1)
    new_pos = curr_pos-int(0.08*(curr_load-curr_pos))
    print("Pos: {} Load: {} New pos {}".format(curr_pos, curr_load, new_pos))
    serial_connection.goto(1, new_pos)
  except:
    pass


