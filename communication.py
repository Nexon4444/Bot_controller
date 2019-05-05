# Import package
import paho.mqtt.client as mqtt
# import mqtt
import time
import re

broker = "192.168.0.103"
port = 1883


class Message(object):
    def __init__(self, name, bot_mov_x, bot_mov_y):
        self.name = name
        self.bot_mov_x = bot_mov_x
        self.bot_mov_y = bot_mov_y

    def print_all(self):
        print (str(self.name) + " : " + str(self.bot_mov_x) + " : " + str(self.bot_mov_y))

class Simple_command(object):
    def __init__(self, swarm_bot_name, command, interval):
        self.swarm_bot_name = swarm_bot_name
        self.command = command
        self.interval = float(interval)
        self.print_all()

    def print_all(self):
        print(str(self.command) + " : " + str(self.interval))

class Communicate(object):

    def __init__(self, swarm_bot, broker_adress, broker_port=port):
        self._set_dicts()
        self.swarm_bot = swarm_bot
        self.broker_adress = broker_adress
        self.broker_port = broker_port
        # self.swarm_bot.read_message()

        self._configure_communicate()

    def _set_dicts(self):
        self.regex = {
            "input_vector": re.compile("(?P<swarm_bot_name>\w*):(?P<bot_mov_x>\d+.\d+):(?P<bot_mov_y>\d+.\d+)"),
            "simple_command":  re.compile("(?P<swarm_bot_name>\w*):(?P<command>\w+):(?P<interval>\d+)")
        }

    def _on_log(self, client, userdata, level, buf):
        print("log: " + str(buf))

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # client.connected_flag = True  # set flag
            print("connected OK")

        else:
            print("Bad connection Returned code=", str(rc))

    def _on_disconnect(self, client, userdata, flags, rc=0):
        print("Disconnected result code " + str(rc))

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8"))
        self.swarm_bot.read_message(self.analyze_simple_message(m_decode))
        print("message received", str(m_decode))

    def analyze_message(self, msg):
        return self._deserialize(msg)

    def analyze_simple_message(self, msg):
        return self._deserialize_simple_cmd(msg)

    # def _switch(self, msg):
    #     return {
    #         'a': 1,
    #         'b': 2,
    #     }[msg]
    '''
    communication pattern:
    [swarm_bot_name][bot_mov_x][bot_mov_y][bot_poz_x][bot_poz_y]
    '''
    def _deserialize_simple_cmd(self, msg):
        matched = re.match(self.regex["simple_command"], msg)
        return Simple_command(self._get_group(matched, "swarm_bot_name"), self._get_group(matched, "command"),
                       self._get_group(matched, "interval"))

    def _deserialize(self, msg):
        matched = re.match(self.regex["input_vector"], msg)
        return Message(self._get_group(matched, "swarm_bot_name"), self._get_group(matched, "bot_mov_x"),
                       self._get_group(matched, "bot_mov_y"))

    # def _serialize(self, swarm_bot):

    def _get_group(self, matched, val):
        print("_get_group: " + str(val))
        return matched.group(val)

    def _configure_communicate(self):
        self.client = mqtt.Client(self.swarm_bot.name)
        self.client.on_connect = self._on_connect
        self.client.on_log = self._on_log
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        print("connecting to broker", str(broker))
        self.client.connect(broker, port)

        # while not client.conne(?P<swarm_bot_name>\w*):(cted_flag: #wait in loop
        #     print("In wait loop")
        #     time.sleep(1)
        self.client.subscribe("swarm_bot2/commands")
        self.client.loop_start()
        # client.loop_forever(200.0)

        # self.client.publish("swarm_bot2/commands", "my first command")
        time.sleep(300)
        self.client.loop_stop()
        self.client.disconnect()
