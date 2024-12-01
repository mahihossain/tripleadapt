
import paho.mqtt.client as mqtt
import threading
import json


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    sensordata=[]
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # Open a file with access mode 'a'
    file_object = open('data.txt', 'a')
    # Append 'hello' at the end of file
    file_object.write(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "\n")
    # Close the file
    file_object.close()
    # sensordata.append({"ax value":msg.payload})
    # with open("data.json", 'w+') as f:
    #     json.dump(sensordata, f)


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


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
mqttc.subscribe("esp32/deeps", 0)

mqttc.loop_forever()