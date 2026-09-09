# embedded-systems-lab

![Wokwi CI](https://github.com/PresidenteOG/embedded-systems-lab/actions/workflows/wokwi-ci.yml/badge.svg)

MicroPython on the ESP32, run in the [Wokwi](https://wokwi.com) simulator. These
are the hardware exercises from my DAM coursework: sensors, actuators, two small
state machines, and three sketches that coordinate over MQTT. One folder per
exercise, each self-contained.

Nothing here has a framework or an architecture, and that is the point. Every
exercise is a single `main.py` sitting next to its wiring. The interesting part
is the hardware handling: reading an ADC, driving a servo with PWM, pacing a
sampling loop, keeping an I2C display in sync, servicing MQTT messages without
stalling the main work.

## Exercises

| Folder | What it practices | Parts |
|--------|-------------------|-------|
| `01-traffic-light` | A three-mode state machine (normal / emergency / out of service) driving a timed LED sequence. Mode is chosen at the serial prompt. | 3 LEDs |
| `02-traffic-light-lcd` | The same state machine, with a 16x2 I2C LCD spelling out the current mode and light states. | 3 LEDs, I2C 1602 LCD |
| `03-dht22-rolling-average` | Sampling a DHT22 every 2 s and reporting a rolling average once per minute (30 samples per window). | DHT22 |
| `04-ldr-window-stats` | Collecting light readings over a 60-sample window, then printing min, mean and max for that window. | Photoresistor |
| `05-temperature-to-servo` | Mapping a temperature reading onto a servo angle with a linear transform, split across the sub-zero and above-zero ranges. | DHT22, servo |
| `06-joystick-dual-servo` | Two analog joystick axes scaled to PWM duty for two independent servos. | Analog joystick, 2 servos |
| `07-ldr-relay-switch` | A light threshold that flips a relay — the "switch on the lamp when it gets dark" exercise. | Photoresistor, relay module |
| `08-micropython-lcd-thermostat` | Temperature and humidity on an I2C LCD, redrawing the screen only when the formatted text actually changed. | DHT22, I2C 1602 LCD |
| `09-mqtt-buzzer-control` | A buzzer driven remotely: a JSON message over MQTT sets frequency, repeats, duration and an on/off flag. | Buzzer |
| `10-mqtt-distance-alarm` | An ultrasonic distance alarm whose threshold and enable flag are set over MQTT, so it retunes without reflashing. | HC-SR04 |
| `11-mqtt-motion-alarm` | A PIR intrusion alarm that is armed and disarmed over MQTT and publishes its state back. | PIR, buzzer, LED |

Comments in the code are in Spanish and Catalan — that is how they were written
for class, and I have left them.

## Running an exercise

Each folder has a `diagram.json`, so the quickest way to see one is to open it on
[wokwi.com](https://wokwi.com) or in the Wokwi VS Code extension, which handle the
MicroPython upload for you.

To run one headless (the way CI does), you have to bake the sketch into the
firmware image first, because `wokwi-cli` boots a bare REPL and does not upload
`main.py`:

```bash
cd 03-dht22-rolling-average
pip install "mp-image-tool-esp32[littlefs]"
curl -fSL https://micropython.org/resources/firmware/ESP32_GENERIC-20260406-v1.28.0.bin -o mp.bin
python -c "open('mp-4m.bin','wb').write(open('mp.bin','rb').read().ljust(0x400000, b'\xff'))"
mp-image-tool-esp32 mp-4m.bin --add vfs=fat:2M:2M --fs mkfs vfs --fs put *.py / -o firmware-fs.bin
wokwi-cli . --scenario scenario.test.yaml
```

`01-` and `02-` read their mode from the serial console — type `NORMAL`,
`EMERGENCIA`, `OUT` (or `FDS` for `02-`) into the serial monitor when it asks.

The three MQTT folders (`09-`, `10-`, `11-`) need a broker. They default to a
local [Mosquitto](https://mosquitto.org/) instance — install it, run `mosquitto -v`,
and point `MQTT_BROKER` in the sketch at an address the simulator can reach. Each
of those folders has its own README with the exact commands. No public broker is
used anywhere.

## Continuous integration

`.github/workflows/wokwi-ci.yml` runs the eight non-MQTT exercises on every push.
Each job downloads MicroPython, bakes that folder's `.py` files into the image,
boots it on a simulated ESP32 through
[`wokwi-ci-action`](https://github.com/wokwi/wokwi-ci-action), and checks the
serial output against the folder's `scenario.test.yaml`. The MQTT exercises are
left out — a headless run has no broker and no second party to talk to.

The workflow needs a `WOKWI_CLI_TOKEN` repository secret (Wokwi CI dashboard →
API token). The badge above stays red until that secret is set.

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Personal and non-commercial use only.
Third-party code (the LCD driver, the MicroPython firmware) is credited in
[ATTRIBUTION.md](ATTRIBUTION.md).
