# from controller.simulator import *
# from controller.information_transfer import *
from model.config import *
from model.bot_components import *
from model.board import *
import os

app_config = None
# # python3/swarm_bot_simulator/resources/app_config.json
# with open(os.path.join("swarm_bot_simulator", "resources", "app_config.json"), "r", encoding="utf-8") as f:
#     app_config = json.load(f)
#
# print(app_config)
# config = Config(app_config)
# config.swarm_bots[0].messenger.subscribe(topic="test") #, message="test dzialaj")
# config.swarm_bots[0].movement.move_prim(5)
# board = Board(config)
try:
    # simulator = Simulator(config)
    e = threading.Event()
    mess = Messenger(1, config, e)
    time.sleep(100)
    # mess.listen()
    # time.sleep(5)
    # me = MessageEncoder()
    # md = MovementData(Vector(0, 1), 90.0, 3, Movement.MOVE_PRIM)
    # message = Message(MTYPE.SIMPLE, md)
    # mess2 = Messenger("server", config, e)
    #
    # mess2.send("1/receive", message)
    # simulator.communicate(BotInfo(bot_info_parsed=config.bot_infos[0], config=config), board)
    # board = json.loads(mess.last_message)
    # print(str(mess.last_message))
    # time.sleep(3)
    print(str(Messenger.create_message_from_string(mess.receiver.last_message)))
    # simulator.simulate()

except e:
    print("Have you started mosquitto.exe?")
    raise e
