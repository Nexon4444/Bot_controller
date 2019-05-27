import paho.mqtt.client as mqtt
import logging
import time
def on_message(client, userdata, msg):
    logging.debug(msg)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # client.connected_flag = True  # set flag
        logging.debug("connected OK")
    else:
        logging.debug("Bad connection Returned code=", rc)


client = mqtt.Client("client")
client.on_message = on_message
client.on_connect = on_connect
client.connect_async("192.168.0.106", port=2000)
client.subscribe("2/receive")
client.loop_start()

client2 = mqtt.Client("client2")
client2.on_connect = on_connect
client2.on_message = on_message
client2.connect_async("192.168.0.106", port=2000)
client2.publish(topic="2/receive", payload="asdasdasdasd")
# time.sleep(50)