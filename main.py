# This example takes the temperature from the Pico's onboard temperature sensor, and displays it on Pico Display Pack, along with a little pixelly graph.
# It's based on the thermometer example in the "Getting Started with MicroPython on the Raspberry Pi Pico" book, which is a great read if you're a beginner!

import machine
import time
from pimoroni import RGBLED, Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import netman
from umqttsimple import MQTTClient
from machine import Pin
from hx711 import HX711

country = 'GB'
ssid = '6B-WiFi'
password = 'MBSJ2021'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.5.94'
client_id = 'PicoWeight'
topic_pub = 'hello'
sensorName = "Load_Cell"
measurment = "Waste mass"
lab = "3D_printing"
equipment = "Waste_Bin_1"
topic = "data_input/" + lab + "/" + equipment +"/" + sensorName +"/"
messeage = {}
messeage["lab"] = lab
messeage["sensor_type"] = sensorName
messeage["machineName"] = equipment
messeage["measurement"] = measurment
    
last_message = 0
message_interval = 5
counter = 0

# set buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# constants set at begining
driver = HX711(d_out=0, pd_sck=1)
offset = - 295
divide = 442.4
weight = 0
w = 0
repeatNum = 5

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
#led = RGBLED(0, 0, 0)
led = RGBLED(6, 7, 8)

# set the display backlight to 50%
display.set_backlight(0.5)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)


colors = [(0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]

# display.circle(ball_x, ball_y, ball_siz_r)
# .rectangle (x, y (top corner), x size, y size)
# .text("text string", x, y, - , size)

#MQTT function
#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# function to read weight sensor N times
def read_weight(repeatNum):
    w = 0
    for i in range(repeatNum):
        w = w + driver.read()
    average = w/repeatNum
    weight = round((average - (95020 + offset*divide))/divide)
    return weight

def sendMess(value, reset):
    messeage["data"] = value
    messeage["reset"] = reset
    mess_send = json.dumps(messeage)
    try:
        client.publish(topic, msg=mess_send)
        display.text("MQTT sent", 5, 5, 0, 2)
        time.sleep(0.5)
        display.text("", 5, 5, 0, 2)
    except:
        try:
            client.disconnect()
            time.sleep(1)
            client.connect()
        except:
            reconnect()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

while True:
    # fills the screen with black
    display.set_pen(BLACK)
    display.clear()
    led.set_rgb(0, 0, 0)
    display.set_pen(WHITE)
    oldWeight = weight
    weight = read_weight(5)
    display.text(str(round(weight/1000, 3)), 10, 20, 0, 7)
    display.text("<--___Zero____-->", 10, 100, 0, 3)
    display.text(" kg", 175, 30, 0, 4)
    # update with new values
    display.update()
    if abs(oldWeight - weight) > 1:  # weight changed by mote than one gram
        sendMess(weight, 0)
    # check for zero button press over 1 second weight
    if button_y.read() or button_b.read():
        offset = offset + weight
        time.sleep(1)
        sendMess(0, 1)
    else:
        time.sleep(0.25)
    
    if button_y.read() or button_b.read():
        offset = offset + weight
        time.sleep(1)
        sendMess(0, 1)
    else:
        time.sleep(0.25)
    