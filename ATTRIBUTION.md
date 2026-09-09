# Attribution

## LCD driver (`lcd_api.py`, `i2c_lcd.py`)

`02-traffic-light-lcd/` and `08-micropython-lcd-thermostat/` bundle two helper
modules for driving an HD44780 character LCD over I2C:

- `lcd_api.py` — the controller command set, from Dave Hylands'
  [`python_lcd`](https://github.com/dhylands/python_lcd) project.
- `i2c_lcd.py` — the PCF8574 I2C backpack HAL from the same project.

Both are used unmodified. They sit in the exercise folder because Wokwi loads
every module from the project directory into the board's filesystem — there is
no package install step in the simulator.

## MicroPython firmware (`firmware/ESP32_GENERIC-20251209-v1.27.0.bin`)

The stock MicroPython build for the generic ESP32, downloaded from
[micropython.org](https://micropython.org/download/ESP32_GENERIC/). MIT-licensed.
It is committed so the simulations run without fetching anything.

## Wokwi wiring for `09-` and `10-`

The `diagram.json` breadboard layouts in `09-mqtt-buzzer-control/` and
`10-mqtt-distance-alarm/` started from a shared Wokwi project by another user
(Wokwi handle *Fadi Korriz*). Each is a single peripheral wired to an ESP32.
The MicroPython code in those folders is mine.
