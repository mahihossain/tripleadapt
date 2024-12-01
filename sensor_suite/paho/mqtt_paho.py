
import paho.mqtt.client as mqtt
import threading
import json


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    sensordata=[]
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    str1 = (msg.payload).decode()
    
    #json.dumps(str1)
    # sensordata.append({"ax value":msg.payload})
    with open("data.json", 'a+') as f:
        json.dump(str1, f,indent=2)
        

# def on_publish(mqttc, obj, mid):
#     print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
# mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("broker.emqx.io", 1883, 60)
mqttc.subscribe("esp32/ta_sensor2", 0)
mqttc.subscribe("esp32/ta_sensor1",0)
mqttc.loop_forever()