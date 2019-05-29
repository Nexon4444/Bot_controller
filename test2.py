import paho.mqtt.client as mqtt
import logging

def on_message(client, userdata, msg):
    logging.debug(msg)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # client.connected_flag = True  # set flag
        logging.debug("connected OK")
    else:
        logging.debug("Bad connection Returned code=", rc)


client = mqtt.Client("client")
client.connect("192.168.0.106")
client.subscribe("2/receive")
client.on_message = on_message
client.loop_forever()