# Traffic light state machine. Pick a mode at the serial prompt:
# NORMAL / EMERGENCIA / OUT.
from machine import Pin
from utime import sleep



Led_Vermell = Pin(15, Pin.OUT)
Led_Groc = Pin(18, Pin.OUT)
Led_Verd = Pin(17, Pin.OUT)


EMERGENCIA = 0

A = input("Seleccion de modo: NORMAL/EMERGENCIA/OUT: ")


if A == "NORMAL":
    while A == "NORMAL":
        Led_Vermell.value(0)
        Led_Verd.value(1)
        sleep(7)
        Led_Verd.value(0)
        Led_Groc.value(1)
        sleep(3)
        Led_Verd.value(0)
        Led_Groc.value(0)
        Led_Vermell.value(1)
        sleep(10)
elif A == "EMERGENCIA":
    while A == "EMERGENCIA" and EMERGENCIA != 3:
        EMERGENCIA += 1
        Led_Groc.value(1)
        sleep(1)
        Led_Groc.value(0)
        sleep(1)
elif A == "OUT":
    print("FUERA DE SERVICIO!")
    while A == "OUT":
        Led_Vermell.value(0) 
        Led_Verd.value(1)
        Led_Groc.value(1)
        sleep(2)
        Led_Vermell.value(1)
        Led_Verd.value(0)
        Led_Groc.value(0)
        sleep(2)
    