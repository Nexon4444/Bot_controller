from robot import Control

class Swarm_bot(object):
    def __init__(self, name):
        self.name = name
        self.parsed_command = None
        self.interval = float(0)
        self.control = Control()

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