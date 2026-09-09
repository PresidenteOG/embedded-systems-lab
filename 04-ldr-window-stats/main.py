import time
import machine

sensor_de_llum = machine.ADC(33)

Tiempo = 0

Tabla = []

while True:

	valor = sensor_de_llum.read()

	time.sleep(1)
	print("Valor del sensor de llum:", valor)

	ValorObtenido = {"Luz": valor}

	Tabla.append(ValorObtenido)

	time.sleep(1)
	Tiempo += 1
	if Tiempo == 60:

		Maximo = max(v["Luz"] for v in Tabla)
		
		Minimo = min(v["Luz"] for v in Tabla)
        
		Mediana = sum(v["Luz"] for v in Tabla) / len(Tabla) 

		print(f"Valor Maximo: {Maximo}")
		print(f"Valor Medio: {Mediana}")
		print(f"Valor Minimo: {Minimo}")
		
		Tabla.clear()
		Tiempo = 0
