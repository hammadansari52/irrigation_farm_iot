import paho.mqtt.client as mqtt
import time


def on_connect(client,userdata, flags, rc):
    if rc==0:
	client.connected_flag=True
    	print("connected with code : "+str(rc))
	client.subscribe("raspberry/topic")
    else:
    	print("Bad connection Returned code = ",rc)

def on_message(client,userdata,msg):
    print(str(msg.payload))



mqtt.Client.connected_flag = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host = "localhost", port=1883, keepalive=60)
client.loop_start() # non-blocking loop, Loop_start starts a loop in another thread and lets the main thread continue

while not client.connected_flag:
	print("in waiting loop")
	time.sleep(1)

for i in range(10):
    client.publish("raspberry/topic", payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_stop()
client.disconnect()