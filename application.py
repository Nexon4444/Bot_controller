from controller.swarm_bot import Swarm_bot
import os
from model.config import *
import argparse
import time
parser = argparse.ArgumentParser(description='Swarmbot')
parser.add_argument('-id', '--bot_id', type=int,
                    help='id of the bot on which we are launching the configuration')

parser.add_argument('-b', '--broker', type=str,
                    help='broker ip address')

parser.add_argument('-p', '--port', type=int,
                    help='broker port')

args = parser.parse_args()
communication_settings = {
    "bot_id": args.bot_id,
    "broker": args.broker,
    "port": args.port,
    "mock": True
}

bot_settings = {
    "max_speed": 5,
    "mode": "1lf"
}

board_settings = {
    "border_x": 2,
    "border_y": 2,
    "side": 20
}

bot_info = {
    "is_real": True,
    "bot_id": args.bot_id,
    "direction": 0,
    "speed": [0, 0],
    "poz_x": 0,
    "poz_y": 0

}

sensor_settings = {
    "1lf": {
        "min_impulse_time": 0.5
    }
}

config = {
    "communication_settings": communication_settings,
    "bot_info": bot_info,
    "bot_settings": bot_settings,
    "board_settings": board_settings,
    "sensor_settings": sensor_settings
}



swarm_bot = Swarm_bot(config)
# mess = Messenger(1, broker=args.broker, port=args.port)
# swarm_bot.start_communication()
print ("attempt to analyze")
swarm_bot.analyze_sensor_data()

time.sleep(10)
print (str(swarm_bot.messenger.get_last_message()))


