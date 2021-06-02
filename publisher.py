import time
import paho.mqtt.publish as publish
while True:
    print("sending 1")
    publish.single("alarme","1",hostname="192.168.1.100")
    time.sleep(6)
    print("sending 0")
    publish.single("alarme","0",hostname="192.168.1.100")
    time.sleep(6)