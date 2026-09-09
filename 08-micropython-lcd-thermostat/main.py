# Thermostat readout on a 16x2 I2C LCD. The screen is only redrawn
# when the formatted text changes.
import dht
import machine
import time

from machine import Pin, SoftI2C
from utime import sleep

#-----
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 45

i2c = SoftI2C (scl=Pin(21), sda=Pin(22), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

pin_dades = machine.Pin(23)
sensor = dht.DHT22(pin_dades)

#CODIGOS DE PANTALLA SACADO:
#https://wokwi.com/projects/380305020528229377
texto_anterior = ""

while True:
    sensor.measure()
    temperatura = sensor.temperature()
    humitat = sensor.humidity()
    texto_mostrar = "Temp: {:.2f}*C\nHumedad: {:.2f}%".format(temperatura, humitat)
    if not texto_anterior == texto_mostrar:
        texto_anterior = texto_mostrar
        lcd.clear()
        lcd.putstr(texto_mostrar)
    if texto_anterior == texto_mostrar:
        print("Igual!")
    sleep(10)
