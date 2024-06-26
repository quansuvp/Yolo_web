import sys
import paho.mqtt.client as mqtt
import time
import random
import serial.tools.list_ports
from uart_hehe import *

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "DADN_232_2024"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2"
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    if(message.topic == "DADN_232_2024/feeds/V1"):
        if(message.payload.decode("utf-8") == "1"):
            uart_write(1)
        elif(message.payload.decode("utf-8") == "0"):
            uart_write(2)
    if(message.topic == "DADN_232_2024/feeds/V1"):
        if(message.payload.decode("utf-8") == "1"):
            uart_write(1)
        elif(message.payload.decode("utf-8") == "0"):
            uart_write(2)

    # print("Received: ", message.payload.decode("utf-8"))
    # print(" Received message " + message.payload.decode("utf-8")
    #       + " on topic '" + message.topic
    #       + "' with QoS " + str(message.qos))
    

def mqtt_published(client, userdata, mid):
    print("Message published with mid: " + str(mid))

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)
        
 #Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message
mqttClient.on_publish = mqtt_published

mqttClient.loop_start()

# counter = 3
# temp = 1
# humi = 1

while True:
    readSerial(mqttClient)
    # counter = counter - 1
    # if counter <= 0:
    #     counter = 3
    #     mqttClient.publish(MQTT_TOPIC_PUB1, temp)
    #     mqttClient.publish(MQTT_TOPIC_PUB2, humi)
    #     temp = temp + 1
    #     humi = humi + 1
    

    time.sleep(1)

    pass



