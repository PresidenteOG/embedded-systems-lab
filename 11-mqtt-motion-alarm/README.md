# 11 — MQTT motion alarm

A PIR sensor guarding a room. Arm or disarm it by sending `Activado` / `Desactivado`
on the control topic. While armed, motion on the PIR sets off the buzzer and a red
LED and the state gets published back over MQTT.

Wiring: PIR on GPIO 23, buzzer on GPIO 13, LED on GPIO 22.

## Running it

Not in the CI matrix — arming happens over MQTT, so it needs a broker.

1. `mosquitto -v` locally.
2. Point `MQTT_BROKER` in `main.py` at an address the Wokwi VM can reach.
3. Start the sim: [wokwi.com](https://wokwi.com/projects/392353697631858689).
4. Arm it: `mosquitto_pub -t InnovationTecnologies_B -m Activado`
5. Trigger the PIR in the simulator and watch `mosquitto_sub -t InnovationTecnologies_A -v`.

The single-letter topics are the original class names.
