# import os
# from google.cloud import pubsub_v1
# from concurrent.futures import TimeoutError

# credentials_path = 'C:/Users/NC/OneDrive/Desktop/PubSub/stellar-orb-274514-9c26c411316a.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# timeout = 5.0

# subscriber = pubsub_v1.SubscriberClient()
# subscription_path = 'projects/stellar-orb-274514/subscriptions/environment_sensors-sub'


# def callback(message):
#     print(f'Received message:{message}')
#     print(f'data: {message.data}')
#     if message.attributes:
#         # print('Attributes:')
#         with open('C:/Users/NC/OneDrive/Desktop/Flask_web_app/res.txt','w') as f:
#             for key in message.attributes:
#                 value = message.attributes.get(key)
#                 f.write(str(key)+ ' ' + str(value)+'\n')
#                 # print(f"{key}: {value}")
#     message.ack()
    
    
# streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
# print(f'Listening for messages on {subscription_path}')

# with subscriber:
#     try:
#         # streaming_pull_future.result(timeout=timeout)
#         streaming_pull_future.result()
#     except TimeoutError:
#         streaming_pull_future.cancel()
#         result =streaming_pull_future.result()



import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "Khang"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1" #cam bien nhiet do
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2" #cam bien do am   
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4" #cam bien anh sang
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"
SOTRAGE1 = 'res1.txt'
SOTRAGE2 = 'res2.txt'
SOTRAGE4 = 'res4.txt'

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)


def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")


def mqtt_recv_message(client, userdata, message):
    print("In recv_message")
    if message.topic == f"{MQTT_TOPIC_PUB1}":
        with open(SOTRAGE1,'w') as f:
            f.write(str(message.topic)+ ' ' + str(message.payload.decode("utf-8"))+'\n')
            f.close()
    elif message.topic == f"{MQTT_TOPIC_PUB2}":
        with open(SOTRAGE2,'w') as f:
            f.write(str(message.topic)+ ' ' + str(message.payload.decode("utf-8"))+'\n')
            f.close()
    elif message.topic == f"{MQTT_TOPIC_PUB4}":
        with open(SOTRAGE4,'w') as f:
            f.write(str(message.topic)+ ' ' + str(message.payload.decode("utf-8"))+'\n')
            f.close()

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)


# Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message= mqtt_recv_message

mqttClient.loop_start()

while True:
    time.sleep(5)
