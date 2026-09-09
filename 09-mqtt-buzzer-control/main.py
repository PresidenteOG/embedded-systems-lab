from machine import Pin, PWM
import utime
from utime import sleep
from umqtt.simple import MQTTClient
import network
import ubinascii
import ujson

buzzer = PWM(Pin(15), freq=440, duty=512)
buzzer.duty(0)

SSID = "Wokwi-GUEST"
PASSWORD = ""
# Point this at your own MQTT broker (see README).
# Default assumes a local Mosquitto instance on this machine.
MQTT_BROKER = "127.0.0.1"
MQTT_TOPIC_PUBLISH = "InnovationTecnologies_BUZZER_PUBLISH" #Enviar MQTT
MQTT_TOPIC_SUBSCRIBE = "InnovationTecnologies_BUZZER_SUBSCRIBE" #Recibir MQTT
CLIENT_ID = "InnovationTechnologies1"

client = MQTTClient(CLIENT_ID, MQTT_BROKER)

#BUZZER SETS
NIVEL_DE_FRECUENCIA = 5000
REPETIR_PITIDO = 6
DURACION_PITIDO = 1
DURACION_ESPERA = 0.5
ACTIVER = 0
POWER = 0

#Wifi
def connect_to_wifi(): 
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        utime.sleep(1)

#Enviar MQTT
def publish_message(topic, message): #Enviar MQTT
    client.connect()
    client.publish(topic, message.encode())

#Mensajes
def callback(topic, msg):  # Mensajes
    global NIVEL_DE_FRECUENCIA, REPETIR_PITIDO, DURACION_PITIDO, DURACION_ESPERA, POWER, ACTIVER
    print("Mensaje recibido en el tópico {}: {}".format(topic, msg))

    # Decodifica el mensaje JSON
    try:
        Datos = ujson.loads(msg)
    except ValueError:
        print("Error al decodificar el mensaje JSON")
        return

    if 'NIVEL_DE_FRECUENCIA' in Datos:
        NIVEL_DE_FRECUENCIA = Datos['NIVEL_DE_FRECUENCIA']
    if 'REPETIR_PITIDO' in Datos:
        REPETIR_PITIDO = Datos['REPETIR_PITIDO']
    if 'DURACION_PITIDO' in Datos:
        DURACION_PITIDO = Datos['DURACION_PITIDO']
    if 'DURACION_ESPERA' in Datos:
        DURACION_ESPERA = Datos['DURACION_ESPERA']
    if 'ACTIVER' in Datos:
        ACTIVER = Datos['ACTIVER']
    if 'POWER' in Datos:
        POWER = Datos['POWER']

    print("NIVEL_DE_FRECUENCIA:", NIVEL_DE_FRECUENCIA)
    print("REPETIR_PITIDO:", REPETIR_PITIDO)
    print("DURACION_PITIDO:", DURACION_PITIDO)
    print("DURACION_ESPERA:", DURACION_ESPERA)
    print("ACTIVER", ACTIVER)
    print("POWER:", POWER)

    publish_message(MQTT_TOPIC_PUBLISH, "Activat")
    subscribe_to_topic()

#Espera de recibir MQTT
def subscribe_to_topic():
    client.set_callback(callback)
    client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    while True:
        print("Esperant resposta...")
        client.check_msg()
        utime.sleep(2)

#Funcion
def ACTIVO():
    publish_message(MQTT_TOPIC_PUBLISH, "Alerta")
    global NIVEL_DE_FRECUENCIA, REPETIR_PITIDO, DURACION_PITIDO, DURACION_ESPERA, POWER
    if POWER == 1:  
        print(TIEMPO_SONIDO)
        for Temps in range(0, REPETIR_PITIDO):
            print("PITIDO")
            sleep(DURACION_ESPERA)
            buzzer.freq(NIVEL_DE_FRECUENCIA)
            buzzer.duty(512)
            sleep(DURACION_PITIDO)
            buzzer.duty(0)

        
connect_to_wifi()
client.connect()
publish_message(MQTT_TOPIC_PUBLISH, "Dispositiu principal conectat")
subscribe_to_topic()