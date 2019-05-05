from controller.robot import Control
import mraa

control = Control()
# control.forward(3)
control.move_front_until_sensor_act()
# while (True):
#     print gpio.read()
#     time.sleep(0.2)