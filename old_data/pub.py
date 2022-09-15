import paho.mqtt.client as mqtt
import time





def on_connect(client,userdata, flags, rc):
    print("connected with code : "+str(rc))
    client.subscribe("raspberry/topic")

def on_message(client,userdata,msg):
    print(str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host = "localhost", port=1883, keepalive=60)
client.loop_start() # non-blocking loop, Loop_start starts a loop in another thread and lets the main thread continue
time.sleep(4) # wait for 4 seconds for the connection to be established and the script will go on after

for i in range(10):
    client.publish("raspberry/topic", payload=i, qos=0, retain=False)
    print(f"send {i} to raspberry/topic")
    time.sleep(1)

client.loop_stop()