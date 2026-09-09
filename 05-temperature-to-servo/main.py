import dht
from machine import Pin,PWM
import utime

#CODIGO REGLA DE 3 OBTENIDO POR:
#https://wokwi.com/projects/382018618012822529

sensor = dht.DHT22(Pin(18))
servo = PWM(Pin(23), freq=50, duty=0)

#duty_min = 40
#duty_max = 115

duty_min = 25
duty_max = 125


while True:
    sensor.measure()
    TEMPERATURA = sensor.temperature()
    if TEMPERATURA < 0:
        TEMPERATURA = (-90/40 * abs(TEMPERATURA) + 90) 
        duty = int((TEMPERATURA /180.0) * (duty_max - duty_min) + duty_min)
        servo.duty(duty)
        print("temp", TEMPERATURA, "-> duty", duty)
        utime.sleep(1)
    elif TEMPERATURA > 0:
        TEMPERATURA = (90 * abs(TEMPERATURA) /80) + 90
        duty = int((TEMPERATURA /180.0) * (duty_max - duty_min) + duty_min)
        servo.duty(duty)
        print("temp", TEMPERATURA, "-> duty", duty)
        utime.sleep(1)
    else:
        servo.duty(75)