# 10 — MQTT distance alarm

An HC-SR04 ultrasonic sensor on an ESP32. It measures distance in a loop and,
when the reading crosses a threshold, publishes an alarm trigger and the distance
to MQTT. The threshold and an on/off flag arrive as a JSON message on the
subscribe topic, so the alarm can be retuned without reflashing.

Wiring: HC-SR04 trig on GPIO 23, echo on GPIO 21.

## Running it

Not in the CI matrix — the alarm logic only makes sense with a broker and a
listener on the other end.

1. `mosquitto -v` on your machine.
2. Set `MQTT_BROKER` in `main.py` to an address the Wokwi VM can reach.
3. Run the sim: [wokwi.com](https://wokwi.com/projects/398686142018515969). Drag the
   HC-SR04 slider to change the distance.
4. Watch the alarm: `mosquitto_sub -t InnovationTecnologies_MICRO_STATS -v`
5. Retune it: `mosquitto_pub -t InnovationTecnologies_MICRO_SUBSCRIBE -m '{"NIVEL_DE_dB": 40, "WAIT": 3, "POWER": 1}'`

`NIVEL_DE_dB` is the distance threshold in cm — the name is left over from an
earlier sound-level version of the exercise.
