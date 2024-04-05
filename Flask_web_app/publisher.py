# import os
# from google.cloud import pubsub_v1

# credentials_path = 'C:/Users/NC/OneDrive/Desktop/PubSub/stellar-orb-274514-9c26c411316a.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# publisher = pubsub_v1.PublisherClient()
# topic_path = 'projects/stellar-orb-274514/topics/environment_sensors'

# data = 'A garden sensor is ready'
# data =data.encode('utf-8')
# attributes= {
#     'temperature': '75.0',
#     'humidity': '60',
#     'pressure': '1',
#     'light': '50',
# }

# future = publisher.publish(topic_path, data, ** attributes)
# print(f'published message id{future.result()}')








import sys
import paho.mqtt.client as mqtt
import time
from random import randint

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "Khang"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2"
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"


def readSerial(mqttClient):
    data1 =randint(20,38)
    print('print published',data1)
    data2 =randint(50,75)
    print('print published',data2)
    data3 = randint(50,88)
    print('print published',data3)
    mqttClient.publish(MQTT_TOPIC_PUB1, data1)
    mqttClient.publish(MQTT_TOPIC_PUB2, data2)
    mqttClient.publish(MQTT_TOPIC_PUB4, data3)


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")


def mqtt_published(client, userdata, mid):
    print("Message published with mid: " + str(mid))

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)
        
 #Register mqtt events
mqttClient.on_connect = mqtt_connected
# mqttClient.on_subscribe = mqtt_subscribed
 # mqttClient.on_message = mqtt_recv_message
mqttClient.on_publish = mqtt_published

mqttClient.loop_start()

while True:
    readSerial(mqttClient)
    time.sleep(5)
    pass

