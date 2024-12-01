import paho.mqtt.client as mqtt
import threading
import json
import datetime

# # clear file
open('data.txt', 'w').close()

class myThread(threading.Thread):
    def __init__(self,threadID,name):
        super(myThread,self).__init__()
        # threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID

    def run(self):
        self.sensor()

    def on_connect(self,mqttc, obj, flags, rc):
        print("rc: " + str(rc))


    def on_message(self,mqttc, obj, msg):
        sensordata=[]
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime('%d-%m-%Y %H:%M:%S.%f')
        incoming_lines = msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "#" + ts + "\n"
        
        print(incoming_lines)
        file_object = open('data.txt', 'a')
        file_object.write(incoming_lines)
        file_object.close()
    # sensordata.append({"ax value":msg.payload})
    # with open("data.json", 'w+') as f:
    #     json.dump(sensordata, f)
    def on_publish(self,mqttc, obj, mid):
        print("mid: " + str(mid))


    def on_subscribe(self,mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
        print("subscribing to Topic: " + self.name)

    def on_log(self,mqttc, obj, level, string):
        print(string)

    def sensor(self):
        mqttc = mqtt.Client()
        mqttc.on_message = self.on_message
        mqttc.on_connect =self.on_connect
        mqttc.on_subscribe = self.on_subscribe

        mqttc.connect("broker.emqx.io", 1883, 60)
        mqttc.subscribe("esp32/"+self.name, 0)
        print("subscribing to Topic: "+self.name)
        mqttc.loop_forever()


thread1=myThread(1,"ta_sensor1")
thread2=myThread(2,"ta_sensor2")
thread3=myThread(3,"ta_sensor3")
thread4=myThread(4,"ta_sensor4")
thread5=myThread(5,"ta_sensor5")
thread6=myThread(6,"ta_sensor6")
thread7=myThread(7,"ta_sensor7")

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()


thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()