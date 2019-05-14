from paho.mqtt.client import Client
from controller.information_transfer import Messenger
from model.config import CommunicationSettings
import threading
import time
client = Client("Publisher")
client.connect(host="localhost", port=2000)
client.publish("test", "is this just fanta sea?")

e = threading.Event()
mes = Messenger(1, CommunicationSettings(port=2000, broker='localhost'), e)
mes.send(topic='test', message="caught in a landslide")
mes.subscribe('test')
client.loop_start()
time.sleep(200)
client.loop_stop()
# publish.single("test", "Hello", hostname="192.168.0.106", port=2000)
# publish.single("Example/topic", "World", hostname="192.168.0.110")

# print("OK")