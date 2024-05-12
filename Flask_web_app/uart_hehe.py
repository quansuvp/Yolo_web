import serial.tools.list_ports
import paho.mqtt.client as mqtt

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "Khang"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1" #cam bien nhiet do
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2" #cam bien do am   
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4" #cam bien anh sang
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM6"

def uart_write(data):
    ser.write(str(data).encode())
    return

def processData(mqttClient, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    # print(splitData)
    if splitData[1] == "T":
        mqttClient.publish(MQTT_TOPIC_PUB1, splitData[2])
        print(splitData[2])
    elif splitData[1] == "H":
        mqttClient.publish(MQTT_TOPIC_PUB2, splitData[2])
        print(splitData[2])
    elif splitData[1] == "L":
        mqttClient.publish(MQTT_TOPIC_PUB4, splitData[2])
        print(splitData[2])
mess = ""

def readSerial(mqttClient):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        # print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            # print(mess[start:end + 1])
            processData(mqttClient, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
                

if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    print(ser)