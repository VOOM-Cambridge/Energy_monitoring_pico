import machine
import netman
import time
import json
from umqttsimple import MQTTClient
from machine import Pin

analog_value = machine.ADC(26)
numSamples = 10
deviceVoltage = 3.3  # Volts sensor
lineVoltage = 230    # Mains voltage
CTRange  = 20        # Amps
threshold = 0.25

country = 'GB'
ssid = '**************'
password = '**************'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.5.87'
client_id = 'PicoWeight'
topic_pub = 'hello'
sensorName = "Energy_Monitoring"
measurment = "current"
lab = "Robot_lab"
equipment = "Robot_1"
topic = "data_input/" + lab + "/" + equipment +"/" + sensorName +"/"
messeage = {}
messeage["lab"] = lab
messeage["sensor_type"] = sensorName
messeage["machineName"] = equipment
messeage["measurement"] = measurment

last_message = 0
message_interval = 5
counter = 0

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

def mqttSend(message):
    try:
        client.publish(topic, msg=message)
        print('published')
        time.sleep(1)
    except:
        reconnect()
        pass
    

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

while True:
    val = 0
    for i in range(numSamples):
        reading = analog_value.read_u16()* 3.3 / 65536
        val = val + reading
    readValue = val/numSamples
    print(readValue)
    voltageVirtualValue = readValue*0.7706 #callibration value used
    voltageVirtualValue = (voltageVirtualValue/1024 * deviceVoltage) / 2
    ACCurrtntValue = voltageVirtualValue*CTRange
    powerValue = ACCurrtntValue*lineVoltage
    machineOn = int(ACCurrtntValue > threshold)
    print(ACCurrtntValue)
    time.sleep(1)
    
    m={}
    m["Power"] = voltageVirtualValue 
    m["data"] = ACCurrtntValue
    mess = json.dumps(m)
    mqttSend(mess)
    

client.disconnect()