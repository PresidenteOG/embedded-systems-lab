from machine import Pin, PWM, ADC
import utime

# Configuració dels pins
joystick_x = ADC(Pin(35))  # Pin analògic per la coordenada X del joystick
joystick_y = ADC(Pin(32))  # Pin analògic per la coordenada Y del joystick

servo_x = PWM(Pin(22), freq=50, duty=0)  # Pin del servomotor
servo_y = PWM(Pin(23), freq=50, duty=0)  # Pin del servomotor

duty_min = 24
duty_max = 126

# Bucle principal
while True:
    x_value = joystick_x.read()
    y_value = joystick_y.read()
    print("x", x_value, "y", y_value)
    servo_position = int(((x_value / 4095) *(duty_min - duty_max)) + duty_max)  # Suposa que el rang del joystick és de 0 a 4095
    servo_x.duty(servo_position)
    servo_position = int(((y_value / 4095) *(duty_min - duty_max)) + duty_max)  # Suposa que el rang del joystick és de 0 a 4095
    servo_y.duty(servo_position)
    utime.sleep(0.1)