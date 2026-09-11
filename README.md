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

| Folder | What it practices | Parts | Open in Wokwi |
|--------|-------------------|-------|---------------|
| `01-traffic-light` | A three-mode state machine (normal / emergency / out of service) driving a timed LED sequence. Mode is chosen at the serial prompt. | 3 LEDs | [Run it](https://wokwi.com/projects/474876180329278465) |
| `02-traffic-light-lcd` | The same state machine, with a 16x2 I2C LCD spelling out the current mode and light states. | 3 LEDs, I2C 1602 LCD | [Run it](https://wokwi.com/projects/474876701094258689) |
| `03-dht22-rolling-average` | Sampling a DHT22 every 2 s and reporting a rolling average once per minute (30 samples per window). | DHT22 | [Run it](https://wokwi.com/projects/474876260425823233) |
| `04-ldr-window-stats` | Collecting light readings over a 60-sample window, then printing min, mean and max for that window. | Photoresistor | [Run it](https://wokwi.com/projects/474876304001509377) |
| `05-temperature-to-servo` | Mapping a temperature reading onto a servo angle with a linear transform, split across the sub-zero and above-zero ranges. | DHT22, servo | [Run it](https://wokwi.com/projects/474876353837233153) |
| `06-joystick-dual-servo` | Two analog joystick axes scaled to PWM duty for two independent servos. | Analog joystick, 2 servos | [Run it](https://wokwi.com/projects/474876406916175873) |
| `07-ldr-relay-switch` | A light threshold that flips a relay — the "switch on the lamp when it gets dark" exercise. | Photoresistor, relay module | [Run it](https://wokwi.com/projects/474876448690411521) |
| `08-micropython-lcd-thermostat` | Temperature and humidity on an I2C LCD, redrawing the screen only when the formatted text actually changed. | DHT22, I2C 1602 LCD | [Run it](https://wokwi.com/projects/474876915807029249) |
| `09-mqtt-buzzer-control` | A buzzer driven remotely: a JSON message over MQTT sets frequency, repeats, duration and an on/off flag. | Buzzer | [Run it](https://wokwi.com/projects/397884328047750145) |
| `10-mqtt-distance-alarm` | An ultrasonic distance alarm whose threshold and enable flag are set over MQTT, so it retunes without reflashing. | HC-SR04 | [Run it](https://wokwi.com/projects/398686142018515969) |
| `11-mqtt-motion-alarm` | A PIR intrusion alarm that is armed and disarmed over MQTT and publishes its state back. | PIR, buzzer, LED | [Run it](https://wokwi.com/projects/392353697631858689) |

Comments in the code are in Spanish and Catalan — that is how they were written
for class, and I have left them.

## What's in each folder

| File | What it is |
|------|------------|
| `main.py` | the exercise |
| `diagram.json` | the wiring — which ESP32 pin connects to which sensor, LED or module |
| `wokwi.toml` | tells Wokwi which firmware to boot and where the code lives |
| `scenario.test.yaml` | the serial lines the exercise is expected to print; CI checks against this |

## Running an exercise

Open the folder on [wokwi.com](https://wokwi.com) — drag `main.py` and
`diagram.json` onto the page — or open it with the Wokwi VS Code extension.
Either way Wokwi flashes MicroPython and runs `main.py` for you; press play and
watch the serial monitor.

`01-` and `02-` wait for you to choose a mode: type `NORMAL`, `EMERGENCIA` or
`OUT` (`FDS` instead of `OUT` on `02-`) into the serial monitor when it prompts.

The three MQTT folders (`09-`, `10-`, `11-`) also need a broker running. They
connect to `127.0.0.1:1883` by default — install
[Mosquitto](https://mosquitto.org/), run `mosquitto -v`, and set `MQTT_BROKER` in
the sketch to an address the simulator can reach. Each of those folders has its
own README with the commands. No public broker anywhere.

## Continuous integration

Every push runs the 8 non-MQTT exercises through
[Wokwi's CI action](https://github.com/wokwi/wokwi-ci-action). It boots each one
on a simulated ESP32 with no UI and compares the serial output, line by line,
against that folder's `scenario.test.yaml`. If a sketch stops printing what it
should, the build turns red — that is what the badge at the top of this file
tracks.

One wrinkle worth knowing: Wokwi's headless runner starts MicroPython at an empty
prompt and doesn't upload `main.py` by itself, so before each run the workflow
packs the folder's `.py` files into the firmware image and boots that instead.
The exact steps are in
[`.github/workflows/wokwi-ci.yml`](.github/workflows/wokwi-ci.yml) — none of it is
needed to run an exercise the normal way described above.

The MQTT exercises sit out CI: a headless run has no broker and no one on the
other end to message.

The workflow reads a `WOKWI_CLI_TOKEN` repository secret, generated from the
[Wokwi CI dashboard](https://wokwi.com/dashboard/ci). The badge stays red until
that secret is set.

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Personal and non-commercial use only.
Third-party code (the LCD driver, the MicroPython firmware) is credited in
[ATTRIBUTION.md](ATTRIBUTION.md).
