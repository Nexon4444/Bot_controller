from controller.information_transfer import Messenger, MTYPE, MSIMPLE, MMACRO
from threading import *

from model.bot_components import BotInfo, Vector
from hardware import Control
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Swarm_bot(object):
    def __init__(self, config):
        self.parsed_command = None
        self.interval = float(0)
        self.sensor_event_1lf = Event()
        self.control = Control(self.sensor_event_1lf, config=config)

        self.mess_event = Event()
        self.messenger = Messenger(config["communication_settings"]["bot_id"],
                                   config["communication_settings"]["broker"],
                                   config["communication_settings"]["port"],
                                   self.mess_event)
                                   # config["communication_settings"]["mock"])
        self.config = config
        self.bot_info = BotInfo(config["bot_info"], config)

    def launch(self):
        self.control.activate_sensors()
        t_analyze_sensor_data = Thread(target=self.analyze_sensor_data)

        t_analyze_sensor_data.start()
        t_analyze_sensor_data.join()

    def log(self, msg):
        logging.debug(msg=msg)

    def read_message(self, simple_command):
        self.interval = float(simple_command.interval)
        self.parsed_command = self.choose_command(simple_command.command)

    def choose_command(self, cmd):
        if (cmd == "lrotate"):
            self.control.lrotate(self.interval)
        elif (cmd == "rrotate"):
            self.control.rrotate(self.interval)
        elif (cmd == "lturn"):
            self.control.lturn(self.interval)
        elif (cmd == "rturn"):
            self.control.rturn(self.interval)
        elif (cmd == "forward"):
            self.control.forward(self.interval)
        elif (cmd == "back"):
            self.control.back(self.interval)

        return cmd

    def start_communication(self):
        t_command = Thread(target=self.acquire_command)
        t_command.start()
        t_command.join()

    def acquire_command(self):
        while True:
            self.mess_event.wait()
            self.execute_command(self.messenger.get_last_message())
            self.mess_event.clear()

    def execute_command(self, command):
        print (MTYPE.SIMPLE)
        print (command.message["command"])
        if command.type == MTYPE.SIMPLE:
            if command.message["command"] == MSIMPLE.FORWARD:
                self.log("Executing command: " + MTYPE.SIMPLE + "." + MSIMPLE.FORWARD)
                self.control.forward(float(command.message["time"]))
            elif command.message["command"] == MSIMPLE.REVERSE:
                self.log("Executing command: " + MTYPE.SIMPLE + "." + MSIMPLE.REVERSE)
                raise NotImplementedError("No reverse")
                # self.control.(float(command.message["time"]))
            elif command.message["command"] == MSIMPLE.TURN_RIGHT:
                self.log("Executing command: " + MTYPE.SIMPLE + "." + MSIMPLE.TURN_RIGHT)
                self.control.rrotate(float(command.message["time"]))
            elif command.message["command"] == MSIMPLE.TURN_LEFT:
                self.log("Executing command: " + MTYPE.SIMPLE + "." + MSIMPLE.TURN_LEFT)
                self.control.lrotate(float(command.message["time"]))

        if command.type == MMACRO.MEAUSURE_LINE:
                self.log("Executing command: " + MTYPE.SIMPLE + "." + MSIMPLE.TURN_LEFT)
                self.control.measure_line()

        if command.type == MTYPE.BOT_INFO:
                self.log("Executing command: " + MTYPE.BOT_INFO + " Dir: " + command.message.dir)


    def analyze_sensor_data(self):
        logging.debug("start: " + str(self.bot_info))
        if self.config["bot_settings"]["mode"] is "1lf":
            while True:
                logging.debug("analyze mode: " + str(self.config["bot_settings"]["mode"]))
                # sensor = self.control.sensors_dict["1lf"]
                self.sensor_event_1lf.wait()
                self.bot_info.position.add_vector(Vector(1, 0))
                logging.debug("movement: " + str(self.bot_info))
                self.sensor_event_1lf.clear()
