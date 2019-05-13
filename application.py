from controller.information_transfer import *
from controller.robot import *
from controller.swarm_bot import Swarm_bot
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
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()
# print args.accumulate(args.integers)


swarm_bot = Swarm_bot(id=args.bot_id, communication_settings=CommunicationSettings(args.broker, args.port))
# swarm_bot.start_communication()
swarm_bot.messenger.subscribe(topic="test")
# mes = Messenger(None, communication_settings=CommunicationSettings(args.broker, args.port), mess_event=None)
# mes.subscribe("test")
swarm_bot.messenger.send(topic="test", message=str("asdqtwgehsyizwHEAioeosf"))
time.sleep(200)
# mes = Messenger(args.bot_id, CommunicationSettings(args.broker, args.port))
# mes.send("1/main", "sdafgwrrwerwe")


