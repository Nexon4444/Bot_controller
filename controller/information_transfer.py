import time
from threading import *
import paho.mqtt.client as mqtt
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Messenger:
    logging_on = False
    logging_mess_on = True

    def __init__(self, name, communication_settings, mess_event):
        self.last_message = ""
        self.name = name
        self.client = mqtt.Client(str(name) + "_client")
        # self.name_topic = name + "/" + topic
        self.client.on_connect = self.on_connect
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.main_channel = "main"
        #threading
        self.mess_event = mess_event
        self.cond = Condition()

        self.log("connecting to broker: " + str(communication_settings.broker))
        self.client.connect(communication_settings.broker, communication_settings.port)

        topic = self.create_topic(str(self.name), str(self.main_channel))
        self.subscribe(topic)
        self.client.loop_start()
        print "loop started!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    def subscribe(self, topic):
        # print  topic
        self.log("\n===========================\nSubscribed: " + topic + "\n===========================")
        self.client.subscribe(topic)
        # print str("1/main").decode("UTF-8")
        # self.client.subscribe(str("1/main").decode("UTF-8"))



    def on_log(self, client, userdata, level, buf):
        self.log(str(self.name) + " log: " + str(buf) + " ")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            # client.connected_flag = True  # set flag
            self.log("connected OK")
        else:
            self.log("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.log("Disconnected result code " + str(rc))

    def on_message(self, client, userdata, msg):
        # topic = msg.topic
        logging.debug("received message: " + str(msg))
        m_decode = str(msg.payload.decode("utf-8"))
        # print("=========++++++++++++=============")
        self.log(str(self.name) + " received message: " + str(m_decode))
        if not Messenger.logging_on and Messenger.logging_mess_on:
            logging.debug(str(self.name) + " received message: " + str(m_decode))

        with self.cond:
            self.last_message = m_decode

        self.mess_event.set()

    def send(self, topic=None, message="DEFAULT"):
        self.log("sending message: " + str(message))
        if topic is None:
            topic = self.create_topic(self.name, self.main_channel)
        # self.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.client.publish(topic=topic, payload=message)


    def create_topic(self, *args):
        return '/'.join(args)

    def log(self, msg):
        if Messenger.logging_on:
            logging.debug(msg)

# def recieve(self):
#     def connection_execute(self):
#         # mqtt.Client.connected_flag=False#create flag in class
#
#         # self.client.loop_forever(200.0)
#
#         self.client.publish("swarm_bot2/commands", "my first command")
#         time.sleep(10)
#         self.client.loop_stop()
#         self.client.disconnect()

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_last_message(self):
        with self.cond:
            return self.last_message
