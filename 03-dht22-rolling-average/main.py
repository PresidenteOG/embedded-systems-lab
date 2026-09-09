import dht #exporta el dht
import machine #exporta la maquina
import time #exporta el tiempo
#TEST https://wokwi.com/projects/322577683855704658

# Configura el pin de dades del sensor d'humitat (GPIO 4, per exemple)
pin_dades = machine.Pin(23) #utiliza la variable pin_dades 
sensor = dht.DHT22(pin_dades)

TimeHours = []
TimeMinutes = []

MinA = 0
MinF = 1
Segundos = 0

while True:
	sensor.measure()
	temperatura = sensor.temperature()  
	humitat = sensor.humidity()
	TimeMinutes.append((temperatura, humitat))
	time.sleep(2)
	Informacion = ("Segundos:",Segundos,"Humedad:",humitat,"Temperatura:",temperatura)
	print(Informacion)
	Segundos += 2
	
	if len(TimeMinutes) == 30:
		PromedioT = sum(A[0] for A in TimeMinutes) / len(TimeMinutes)
		PromedioH = sum(A[1] for A in TimeMinutes) / len(TimeMinutes)
		TimeHours.append(("Minuto inicial",MinA,"Minuto final",MinF,"Temperatura Promedio", PromedioT,"Humedad Promedio",PromedioH))
		MinA +=1
		MinF +=1
		print(TimeHours)
		TimeHours = []
		Informacion = []
		Segundos = 0
		TimeMinutes = [(MinA,MinF)]

#CODIGO HECHO POR DANIEL ADANEGBE MOLINA
