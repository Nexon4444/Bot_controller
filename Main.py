from communication import Communicate
from controller.swarm_bot import Swarm_bot
# from robot import Control

print ("executing bot control")

#!/usr/bin/python


def main():
    robot_name = "swarm_bot2"
    broker_adr = "192.168.0.103"
    port = 1883

    # control = Control()
    # control.forward(1)
    swarm_bot2 = Swarm_bot("swarm_bot2")
    com = Communicate(swarm_bot2, broker_adr)
    # m = com.analyze_message("you_touch_my_shialala:19.20:39.34", "input_vector")
    # m2 = com.analyze_simple_message("you_touch_my_shialala:ma_ding_dong:4")
    # print(m)
    # m2.print_all()


if __name__ == '__main__':
    main()


# print( "executing example")
# import sys
#
# sys.path.append(r'~/programy/python/')
#
# from robot import *
# print("forward")
# forward(1)
# print("lrotate")
# lrotate(1)
# print("forward")
# forward(1)
# print("lrotate")
# lrotate(1)
# back(1)
# rrotate(1)
# back(1)
# rrotate(1)
#
# quit()
