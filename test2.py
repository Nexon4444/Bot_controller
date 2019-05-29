import paho.mqtt.client as mqtt
import logging
import time
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def on_message(client, userdata, msg):
    logging.debug(msg)

client = mqtt.Client("client")
client.connect("192.168.0.106", port=2000)
client.subscribe("2/receive")
client.on_message = on_message
client.loop_start()
time.sleep(100)
client.loop_stop()