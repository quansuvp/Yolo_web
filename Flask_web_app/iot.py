from event_manager import *
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from aiot_lcd1602 import LCD1602
from mqtt import *
from aiot_rgbled import RGBLed
from machine import RTC
import ntptime
import time

event_manager.reset()

aiot_dht20 = DHT20(SoftI2C(scl=Pin(22), sda=Pin(21)))

aiot_lcd1602 = LCD1602()

def on_event_timer_callback_d_S_r_j_D():
  global th_C3_B4ng_tin, RT, GDD, RH, SM, LUX
  aiot_dht20.read_dht20()
  RT = aiot_dht20.dht20_temperature()
  RH = aiot_dht20.dht20_humidity()
  SM = round(translate((pin1.read_analog()), 0, 4095, 0, 100))
  LUX = round(translate((pin2.read_analog()), 0, 4095, 0, 100))
  aiot_lcd1602.move_to(0, 0)
  aiot_lcd1602.putstr('RT:')
  aiot_lcd1602.move_to(3, 0)
  aiot_lcd1602.putstr(RT)
  aiot_lcd1602.move_to(7, 0)
  aiot_lcd1602.putstr('*C')
  aiot_lcd1602.move_to(10, 0)
  aiot_lcd1602.putstr('RH:')
  aiot_lcd1602.move_to(13, 0)
  aiot_lcd1602.putstr(RH)
  aiot_lcd1602.move_to(15, 0)
  aiot_lcd1602.putstr('%')
  aiot_lcd1602.move_to(0, 1)
  aiot_lcd1602.putstr('LUX:')
  aiot_lcd1602.move_to(4, 1)
  aiot_lcd1602.putstr(LUX)
  aiot_lcd1602.move_to(6, 1)
  aiot_lcd1602.putstr('%')
  aiot_lcd1602.move_to(9, 1)
  aiot_lcd1602.putstr('SM:')
  aiot_lcd1602.move_to(13, 1)
  aiot_lcd1602.putstr(SM)
  aiot_lcd1602.move_to(15, 1)
  aiot_lcd1602.putstr('%')
  mqtt.publish('V1', RT)
  mqtt.publish('V2', RH)
  mqtt.publish('V3', SM)
  mqtt.publish('V4', LUX)

event_manager.add_timer_event(5000, on_event_timer_callback_d_S_r_j_D)

def on_mqtt_message_receive_callback__V10_(th_C3_B4ng_tin):
  global RT, GDD, RH, SM, LUX
  if th_C3_B4ng_tin == '1':
    pin10.write_digital((1))
  else:
    pin10.write_digital((0))

tiny_rgb = RGBLed(pin0.pin, 4)

def on_mqtt_message_receive_callback__V11_(th_C3_B4ng_tin):
  global RT, GDD, RH, SM, LUX
  if th_C3_B4ng_tin == '1':
    tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  else:
    tiny_rgb.show(0, hex_to_rgb('#000000'))

def on_mqtt_message_receive_callback__V6_(th_C3_B4ng_tin):
  global RT, GDD, RH, SM, LUX
  if th_C3_B4ng_tin == 'AnhNen':
    print('{' + 'AnhNen' + ': ' + str(0) + '}')
    tiny_rgb.show(0, hex_to_rgb('#000000'))
  elif th_C3_B4ng_tin == 'LaVang':
    print('{' + 'LaVang' + ': ' + str(0) + '}')
    tiny_rgb.show(0, hex_to_rgb('#ffff00'))
  elif th_C3_B4ng_tin == 'LaXanh':
    print('{' + 'LaXanh' + ': ' + str(0) + '}')
    tiny_rgb.show(0, hex_to_rgb('#00ff00'))
  elif th_C3_B4ng_tin == 'LaSau':
    print('{' + 'LaSau' + ': ' + str(0) + '}')
    tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  elif th_C3_B4ng_tin == 'QuaXanh':
    print('{' + 'QuaXanh' + ': ' + str(0) + '}')
    pin4.servo_write(0)
  else:
    print('{' + 'QuaVang' + ': ' + str(0) + '}')
    pin4.servo_write(90)

# Mô tả hàm này...
def _C4_90_C4_83ng_k_C3_AD_server():
  global th_C3_B4ng_tin, RT, GDD, RH, SM, LUX, aiot_dht20, tiny_rgb, aiot_lcd1602
  mqtt.on_receive_message('V10', on_mqtt_message_receive_callback__V10_)
  mqtt.on_receive_message('V11', on_mqtt_message_receive_callback__V11_)
  mqtt.on_receive_message('V6', on_mqtt_message_receive_callback__V6_)

def on_event_timer_callback_s_q_q_B_G():
  global th_C3_B4ng_tin, RT, GDD, RH, SM, LUX
  if (round(translate((pin2.read_analog()), 0, 4095, 0, 100))) >= 50:
    GDD = (GDD if isinstance(GDD, (int, float)) else 0) + 1
    mqtt.publish('V5', GDD)

event_manager.add_timer_event(5000, on_event_timer_callback_s_q_q_B_G)

if True:
  display.scroll('hi')
  mqtt.connect_wifi('Tien Trung', '0914020981')
  mqtt.connect_broker(server='mqtt.ohstem.vn', port=1883, username='DADN_232_2024', password='')
  ntptime.settime()
  (year, month, mday, week_of_year, hour, minute, second, milisecond) = RTC().datetime()
  RTC().init((year, month, mday, week_of_year, hour+7, minute, second, milisecond))
  aiot_lcd1602.clear()
  _C4_90_C4_83ng_k_C3_AD_server()
  GDD = 0
  mqtt.publish('V5', GDD)
  display.scroll('ok')

while True:
  mqtt.check_message()
  event_manager.run()
  time.sleep_ms(1000)