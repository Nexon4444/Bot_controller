from paho.mqtt.client import Client


client = Client("Publisher")
client.connect(host="192.168.0.106", port=2000)
client.publish("test", "test message")
# publish.single("test", "Hello", hostname="192.168.0.106", port=2000)
# publish.single("Example/topic", "World", hostname="192.168.0.110")

# print("OK")