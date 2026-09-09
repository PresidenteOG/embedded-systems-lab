from machine import Pin, PWM
import utime
from utime import sleep
from umqtt.simple import MQTTClient
import network
import ubinascii

buzzer = PWM(Pin(13), freq=440, duty=512)
Movement = Pin(23, Pin.IN, Pin.PULL_DOWN)
Led_Vermell = Pin(22, Pin.OUT)
buzzer.duty(0)

SSID = "Wokwi-GUEST"
PASSWORD = ""
# Point this at your own MQTT broker (see README).
# Default assumes a local Mosquitto instance on this machine.
MQTT_BROKER = "127.0.0.1"
MQTT_TOPIC = "InnovationTecnologies_A"
MQTT_TOPIC2 = "InnovationTecnologies_B"
CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac')[-3:]).decode()

client = MQTTClient(CLIENT_ID, MQTT_BROKER)

LECTOR = 0
alarma_activa = True

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        utime.sleep(1)

def publish_message(topic, message):
    client.connect()
    client.publish(topic, message.encode())

def callback(topic, msg):
    global LECTOR, alarma_activa
    print("Received message on topic {}: {}".format(topic, msg))
    Decoder = msg.decode('utf-8')
    print(Decoder)
    if topic.decode('utf-8') == MQTT_TOPIC2:
        if Decoder == "Activado":
            alarma_activa = True
            publish_message(MQTT_TOPIC, "Activo")
            LECTOR = 1
            print("Alarma Activada")
            ARRANQUE()
        elif Decoder == "Desactivado":
            alarma_activa = False
            LECTOR = 0
            publish_message(MQTT_TOPIC, "Desactivado")
            print("Alarma Desactivada")
    subscribe_to_topic()

def subscribe_to_topic():
    client.set_callback(callback)
    client.subscribe(MQTT_TOPIC2)
    while True:
        print("Esperando Respuesta...")
        client.subscribe(MQTT_TOPIC2)
        client.check_msg()
        utime.sleep(1)

def ALERTA():
    global LECTOR, alarma_activa
    while LECTOR == 1 and alarma_activa:
        Led_Vermell.value(1)
        buzzer.freq(5000)
        buzzer.duty(512)
        sleep(0.5)
        Led_Vermell.value(0)
        buzzer.duty(0)
        sleep(0.5)
        client.set_callback(callback)
        client.subscribe(MQTT_TOPIC2)
        client.check_msg()

def ARRANQUE():
    global LECTOR, alarma_activa
    estado = Movement.value()
    while LECTOR > 0:
        estado = Movement.value()
        print(estado)
        if estado == 1:
            print("Intruso detectado!")
            sleep(1)
            ALERTA()
            break
        client.set_callback(callback)
        client.subscribe(MQTT_TOPIC2)
        client.check_msg()
        utime.sleep(1)
    print("DESACTIVANDO!")

connect_to_wifi()
client.connect()
publish_message(MQTT_TOPIC, "Esperando Respuesta")
subscribe_to_topic()