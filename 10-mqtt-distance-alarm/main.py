from machine import Pin
import utime
from umqtt.simple import MQTTClient
import network
import ubinascii
import ujson

SSID = "Wokwi-GUEST"
PASSWORD = ""
# Point this at your own MQTT broker (see README).
# Default assumes a local Mosquitto instance on this machine.
MQTT_BROKER = "127.0.0.1"
MQTT_TOPIC_PUBLISH = "InnovationTecnologies_MICRO_PUBLISH"
MQTT_TOPIC_SUBSCRIBE = "InnovationTecnologies_MICRO_SUBSCRIBE"
CLIENT_ID = "InnovationTechnologies2"
client = MQTTClient(CLIENT_ID, MQTT_BROKER)

MQTT_TOPIC_PUBLISH2 = "InnovationTecnologies_MICRO_STATS"
MQTT_TOPIC_TRIGGER = "InnovationTecnologies_BUZZER_TRIGGER"

# MICROFONO SETS
dB = 55
WAIT = 5
POWER = 1

trig_pin = Pin(23, Pin.OUT)
echo_pin = Pin(21, Pin.IN)

def connect_to_wifi():  # Wifi
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        utime.sleep(1)
    print("Conectado")

def publish_message(topic, message):  # Enviar MQTT
    client.publish(topic, message.encode())

def callback(topic, msg):  # Mensajes
    global dB, WAIT, POWER
    print("Mensaje recibido en el tópico {}: {}".format(topic, msg))
    
    # Decodifica el mensaje JSON
    try:
        data_dict = ujson.loads(msg)
    except ValueError:
        print("Error al decodificar el mensaje JSON")
        return

    if 'NIVEL_DE_dB' in data_dict:
        dB = data_dict['NIVEL_DE_dB']
        print("Nuevo NIVEL_DE_dB:", dB)
    if 'POWER' in data_dict:
        POWER = data_dict['POWER']
        print("Nuevo POWER:", POWER)
    if 'WAIT' in data_dict:
        WAIT = data_dict['WAIT']
        print("Nuevo WAIT:", WAIT)
        
#Señal de ultrasonidos
def read_distance():  
    trig_pin.on()
    utime.sleep_us(10)
    trig_pin.off()

    while echo_pin.value() == 0:
        pulse_start = utime.ticks_us()

    while echo_pin.value() == 1:
        pulse_end = utime.ticks_us()

    duration = pulse_end - pulse_start

    distance = (duration * 0.0343) / 2  
    return distance

#Funcion
def Arranque():
    connect_to_wifi()
    client.connect()
    client.set_callback(callback)
    client.subscribe(MQTT_TOPIC_SUBSCRIBE)

    while True:
        global dB, POWER , WAIT
        client.check_msg()
        if POWER == 1:
            distance = read_distance()
            print(distance, "cm")
            if distance >= dB:
                print("ALARMA!")
                publish_message(MQTT_TOPIC_TRIGGER, "1")
                publish_message(MQTT_TOPIC_PUBLISH2, f"{distance:.2f}")
                utime.sleep(WAIT)
            else:
                publish_message(MQTT_TOPIC_PUBLISH2, f"{distance:.2f}")
            utime.sleep(1) 
        else:
            utime.sleep(1)
Arranque()
