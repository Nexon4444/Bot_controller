from controller.swarm_bot import Swarm_bot
import os
from model.config import *
import argparse
from controller.information_transfer import Messenger
import time
parser = argparse.ArgumentParser(description='Swarmbot')
parser.add_argument('-id', '--bot_id', type=int,
                    help='id of the bot on which we are launching the configuration')

parser.add_argument('-b', '--broker', type=str,
                    help='broker ip address')

parser.add_argument('-p', '--port', type=int,
                    help='broker port')

args = parser.parse_args()
e = threading.Event()
mess = Messenger(1, broker=args.broker, port=args.port, mess_event=e)
time.sleep(10)
print (str(mess.get_last_message()))


