# Traffic light state machine with a 16x2 I2C LCD showing the mode.
# Pick a mode at the serial prompt: NORMAL / EMERGENCIA / FDS.
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

#CODIGOS DE PANTALLA SACADO:
#https://wokwi.com/projects/380305020528229377

Led_Vermell = Pin(15, Pin.OUT)
Led_Groc = Pin(18, Pin.OUT)
Led_Verd = Pin(17, Pin.OUT)


EMERGENCIA = 0
A = input("Seleccion de modo: NORMAL/EMERGENCIA/FDS: ")

if A == "NORMAL":
    while A == "NORMAL":
        Led_Vermell.value(0)
        Led_Verd.value(1)
        lcd.clear()
        lcd.putstr("Modo NORMAL\nR:Off G:Off V:On")
        sleep(7)
        Led_Verd.value(1)
        Led_Groc.value(1)
        lcd.clear()
        lcd.putstr("Modo NORMAL\nR:Off G:On V:On")
        sleep(3)
        Led_Verd.value(0)
        Led_Groc.value(0)
        Led_Vermell.value(1)
        lcd.clear()
        lcd.putstr("Modo NORMAL\nR:On G:Off V:Off")
        sleep(10)
elif A == "EMERGENCIA":
    while A == "EMERGENCIA" and EMERGENCIA != 3:
        EMERGENCIA += 1
        Led_Groc.value(1)
        lcd.clear()
        lcd.putstr("Modo EMERGENCIA\nR:Off G:ON V:Off")
        sleep(1)
        Led_Groc.value(0)
        lcd.clear()
        lcd.putstr("Modo EMERGENCIA\nR:Off G:Off V:Off")
        sleep(1)
elif A == "FDS":
    print("FUERA DE SERVICIO!")
    while A == "FDS":
        Led_Vermell.value(0) 
        Led_Verd.value(1)
        Led_Groc.value(1)
        lcd.clear()
        lcd.putstr("Modo FDS!\nR:Off G:On V:On")
        sleep(2)
        Led_Vermell.value(1)
        Led_Verd.value(0)
        Led_Groc.value(0)
        lcd.clear()
        lcd.putstr("Modo FDS!\nR:On G:Off V:Off")
        sleep(2)
    