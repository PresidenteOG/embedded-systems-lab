import machine
import time


rele = machine.Pin(23, machine.Pin.OUT)
sensor_de_llum = machine.ADC(34)

while True:
    valor = sensor_de_llum.read()
    if valor > 500:
        print("Mayor!")
        rele.value(1)
        time.sleep(1)
    elif valor < 500:
        print("Menor!")
        rele.value(0)
        time.sleep(1)