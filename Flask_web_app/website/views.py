from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .import db
from random import randint
import json
import paho.mqtt.client as mqtt
import time


SOTRAGE1 = 'res1.txt'
SOTRAGE2 = 'res2.txt'
SOTRAGE4 = 'res4.txt'

views = Blueprint('views',__name__)

temperature = 0
humidity = 0 
light = 0
light_mode = False

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "Khang"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB1 = MQTT_USERNAME + "/feeds/V1" #cam bien nhiet do
MQTT_TOPIC_PUB2 = MQTT_USERNAME + "/feeds/V2" #cam bien do am   
MQTT_TOPIC_PUB4 = MQTT_USERNAME + "/feeds/V4" #cam bien anh sang
MQTT_TOPIC_PUB5 = MQTT_USERNAME + "/feeds/V5"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/#"

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)


def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_published(client, userdata, mid):
    print("Message published with mid: " + str(mid))

def mqtt_recv_message(client, userdata, message):
    global temperature, humidity, light
    print("In recv_message")
    if message.topic == f"{MQTT_TOPIC_PUB1}":
        temperature = str(message.payload.decode("utf-8"))
    elif message.topic == f"{MQTT_TOPIC_PUB2}":
        humidity = str(message.payload.decode("utf-8"))
    elif message.topic == f"{MQTT_TOPIC_PUB4}":
        light = temperature = str(message.payload.decode("utf-8"))
    return temperature, humidity, light


mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)


# Register mqtt events
mqttClient.on_publish = mqtt_published
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message= mqtt_recv_message

mqttClient.loop_start()

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note= request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user = current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({'success': True})

@views.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html',user = current_user)

@views.route('/model',methods=['GET','POST'])
def model():
    return render_template('model.html',user = current_user)

@views.route('/dashboardupdate',methods=['GET','POST'])
def get_sensor_reading():
    pressure = 1
    return jsonify({
        'temperature':temperature,
        'pressure':pressure,
        'humidity':humidity,
        'light':light,
    })

@views.route('/lightupdate',methods=['GET','POST'])
def get_light_button():
    data = request.get_json()
    signal = data['isLightOn']
    mqttClient.publish(MQTT_TOPIC_PUB5, signal)
    return jsonify({
        'signal': signal,
    })