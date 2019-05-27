import paho.mqtt.client as mqtt
import logging

def on_message(client, userdata, msg):
    logging.debug(msg)

client = mqtt.Client("client")
client.connect("192.168.0.106")
client.subscribe("2/receive")
client.on_message = on_message
client.loop_forever()