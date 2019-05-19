from controller.information_transfer import Messenger, MTYPE, MSIMPLE
from threading import *
from robot import Control
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Swarm_bot(object):
    def __init__(self, id, broker, port):
        self.parsed_command = None
        self.interval = float(0)
        self.control = Control()
        self.mess_event = Event()
        self.messenger = Messenger(id, broker, port, self.mess_event)

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

