import paho.mqtt.publish as publish


publish.single("test", "Hello", hostname="192.168.0.106")
# publish.single("Example/topic", "World", hostname="192.168.0.110")

# print("OK")