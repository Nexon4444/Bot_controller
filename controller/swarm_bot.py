from controller.information_transfer import Messenger
from threading import *
from robot import Control

class Swarm_bot(object):
    def __init__(self, id, communication_settings):
        self.parsed_command = None
        self.interval = float(0)
        self.control = Control()
        self.mess_event = Event()
        self.messenger = Messenger(id, communication_settings, self.mess_event)

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

    def execute_command(self, parsed_command):
        print (str(parsed_command))
