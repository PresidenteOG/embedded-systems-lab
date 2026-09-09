# 09 — MQTT buzzer control

An ESP32 that keeps a buzzer and waits for commands over MQTT. A JSON payload on
the subscribe topic sets the beep frequency, how many beeps, how long each one
lasts and the gap between them, then `POWER`/`ACTIVER` decide whether it actually
sounds. It publishes a short status string back after each message.

Wiring: buzzer on GPIO 15. Nothing else.

## Running it

This one is not in the CI matrix — it needs a broker and a second party sending
commands, which the headless simulator can't provide. To try it:

1. Install Mosquitto and run it locally: `mosquitto -v`.
2. Edit `MQTT_BROKER` in `main.py` to your machine's address (the Wokwi VM
   can't see `127.0.0.1`; use the LAN IP, or a tunnel).
3. Start the simulation at [wokwi.com](https://wokwi.com/projects/397884328047750145).
4. Publish a command, e.g.
   `mosquitto_pub -t InnovationTecnologies_BUZZER_SUBSCRIBE -m '{"NIVEL_DE_FRECUENCIA": 3000, "REPETIR_PITIDO": 4, "DURACION_PITIDO": 1, "DURACION_ESPERA": 0.5, "ACTIVER": 1, "POWER": 1}'`

The topics (`InnovationTecnologies_*`) are historical names from the original
class project.
