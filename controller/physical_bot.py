# # from controller.information_transfer import Messenger, MTYPE, MSIMPLE, MMACRO
# import controller.information_transfer as it
# from threading import *
#
# from model.bot_components import BotInfo, Vector, Bot
# from hardware import Control
# import logging
# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-10s) %(message)s',
#                     )
#
# class Physical_bot(object):
#     def __init__(self, config):
#         self.bot_id = config.bot_infos[0].bot_id
#         self.parsed_command = None
#         self.interval = float(0)
#         self.sensor_event_1lf = Event()
#         self.control = Control(self.sensor_event_1lf, config=config)
#
#         self.mess_event = Event()
#         self.messenger = it.Messenger(self.bot_id,
#                                    config.communication_settings.broker,
#                                    config.communication_settings.port,
#                                    self.mess_event)
#                                    # config["communication_settings"]["mock"])
#         self.config = config
#         self.bot_info = BotInfo(config.bot_infos[0])j
#         self.time_per_degree = 0.002
#         self.time_per_distance = 0.5
#
#     def launch(self):
#         self.control.activate_sensors()
#         t_analyze_sensor_data = Thread(target=self.analyze_sensor_data)
#
#         t_analyze_sensor_data.start()
#         t_analyze_sensor_data.join()
#
#     def log(self, msg):
#         logging.debug(msg=msg)
#
#     def read_message(self, simple_command):
#         self.interval = float(simple_command.interval)
#         self.parsed_command = self.choose_command(simple_command.command)
#
#     def choose_command(self, cmd):
#         if (cmd == "lrotate"):
#             self.control.lrotate(self.interval)
#         elif (cmd == "rrotate"):
#             self.control.rrotate(self.interval)
#         elif (cmd == "lturn"):
#             self.control.lturn(self.interval)
#         elif (cmd == "rturn"):
#             self.control.rturn(self.interval)
#         elif (cmd == "forward"):
#             self.control.forward(self.interval)
#         elif (cmd == "back"):
#             self.control.back(self.interval)
#
#         return cmd
#
#     def start_communication(self):
#         t_command = Thread(target=self.acquire_command)
#         t_command.start()
#         t_command.join()
#
#     def acquire_command(self):
#         while True:
#             self.mess_event.wait()
#             self.execute_command(self.messenger.get_last_message())
#             self.mess_event.clear()
#
#     def execute_command(self, command):
#         print (it.MTYPE.SIMPLE)
#         print (command.content)
#         if command.type == it.MTYPE.SIMPLE:
#             if command.content["command"] == it.MSIMPLE.FORWARD:
#                 self.log("Executing command: " + it.MTYPE.SIMPLE + "." + it.MSIMPLE.FORWARD)
#                 self.control.forward(float(command.content["time"]))
#             elif command.content["command"] == it.MSIMPLE.REVERSE:
#                 self.log("Executing command: " + it.MTYPE.SIMPLE + "." + it.MSIMPLE.REVERSE)
#                 raise NotImplementedError("No reverse")
#                 # self.control.(float(command.content["time"]))
#             elif command.content["command"] == it.MSIMPLE.TURN_RIGHT:
#                 self.log("Executing command: " + it.MTYPE.SIMPLE + "." + it.MSIMPLE.TURN_RIGHT)
#                 self.control.rrotate(float(command.content["time"]))
#             elif command.content["command"] == it.MSIMPLE.TURN_LEFT:
#                 self.log("Executing command: " + it.MTYPE.SIMPLE + "." + it.MSIMPLE.TURN_LEFT)
#                 self.control.lrotate(float(command.content["time"]))
#
#         if command.type == it.MMACRO.MEASURE_LINE:
#                 self.log("Executing command: " + it.MTYPE.SIMPLE + "." + it.MSIMPLE.TURN_LEFT)
#                 self.control.measure_line()
#
#         if command.type == it.MTYPE.BOT_INFO:
#                 self.log("Executing command: " + it.MTYPE.BOT_INFO + " Dir: " + str(command.content.dir))
#
#         if command.type == it.MTYPE.BOARD:
#                 # self.log("Executing command: " + it.MTYPE.BOARD + " " + str(command.content.bots_info["1"]))
#                 self.log("Bot_info: " + str(command.content.get_bot_info(self.bot_info.bot_id)))
#                 self.steer(command.content.get_bot_info(self.bot_info.bot_id))
#                 bot = Bot(config=self.config, bot_id=self.bot_id
#                           )
#
#
#     def analyze_sensor_data(self):
#         logging.debug("start: " + str(self.bot_info))
#         if self.config["bot_settings"]["mode"] is "1lf":
#             while True:
#                 logging.debug("analyze mode: " + str(self.config["bot_settings"]["mode"]))
#                 # sensor = self.control.sensors_dict["1lf"]
#                 self.sensor_event_1lf.wait()
#                 self.bot_info.position.add_vector(Vector(1, 0))
#                 logging.debug("movement: " + str(self.bot_info))
#                 self.sensor_event_1lf.clear()
#
#     def direct(self, bot_info):
#         diff = bot_info.dir - self.bot_info.dir
#         if diff > 0:
#             self.control.rrotate(self.calc_time_from_dir(diff))
#         else:
#             self.control.lrotate(self.calc_time_from_dir(diff))
#
#         # bot_info.dir - bot_info.dir
#
#     def move(self, bot_info):
#         self.calc_time_for_length(bot_info.speed.magnitude())
#
#     def calc_time_for_length(self, length):
#         return length/self.time_per_distance
#
#     def calc_time_from_dir(self, dir):
#         return dir/self.time_per_degree
#
#     def steer(self, bot_info):
#         self.direct(bot_info)
#         self.move(bot_info)
