import sys
import paho.mqtt.client as mqtt
import time
import random

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "Khang"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1" #cam bien nhiet do
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2" #cam bien do am   
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4" #cam bien anh sang
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)


def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")


def mqtt_recv_message(client, userdata, message):
    # print("Received: ", message.payload.decode("utf-8"))
    # print(" Received message " + message.payload.decode("utf-8")
    #       + " on topic '" + message.topic
    #       + "' with QoS " + str(message.qos))
    if message.topic == f"{MQTT_TOPIC_PUB1}":
        print("Received message " + message.payload.decode("utf-8")
            + " on topic '" + message.topic
            + "' with QoS " + str(message.qos)
            )
    elif message.topic == f"{MQTT_TOPIC_PUB2}":
        print("Received message " + message.payload.decode("utf-8")
            + " on topic '" + message.topic  + "\n"
            + "' with QoS " + str(message.qos)
            )
    elif message.topic == f"{MQTT_TOPIC_PUB4}":
        print("Received message " + message.payload.decode("utf-8")
            + " on topic '" + message.topic  + "\n"
            + "' with QoS " + str(message.qos)
            )


mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)


# Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message= mqtt_recv_message

mqttClient.loop_start()

while True:
    time.sleep(1)