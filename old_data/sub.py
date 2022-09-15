#subscriber file
import paho.mqtt.client as mqtt
import time
import tensorflow as tf
import numpy as np

def on_connect(client,userdata,flags,rc):
    print(f"connected with status code {rc}")	
    client.subscribe("bachelors/sensor_values")
    client.subscribe("bachelors/prediction")


def on_message(client,userdata, msg):
    # print(f"{msg.topic} {msg.payload}")
    if msg.topic == "bachelors/sensor_values":
        print(f"{msg.topic} {msg.payload}") 
        
        txt1 = str(msg.payload).split("'")
        if txt1[1] != 'null':
            txt = txt1[1].split("_")
            humidity = float(txt[1])
            temperature = float(txt[2])
            sensed_values = np.array([[humidity, temperature]])

            ml_model = tf.keras.models.load_model("iot_pred.model")
            prediction = abs(ml_model.predict(sensed_values))
            pl = str(prediction[0][0])

        # txt = txt1.split("_")
        # print("checking-----" + txt[1])
        # if txt[1] != 'null':
        #     humidity = float(txt[1])
        #     temperature = float(txt[2])
        #     sensed_values = np.array([[humidity, temperature]])

        #     ml_model = tf.keras.models.load_model("iot_pred.model")
        #     prediction = abs(ml_model.predict(sensed_values))
        #     pl = str(prediction[0][0])

        else:
            pl = "null"

        time.sleep(1)
        client.publish("bachelors/prediction", payload=pl, qos=0, retain=False)
    # time.sleep(1)

client = mqtt.Client()
client.connect("192.168.137.250",1883,60) #add ip address of the server, localhost gives the self ip address
# client.connect("192.168.214.75",1883,60) #add ip address of the server, localhost gives the self ip address
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()