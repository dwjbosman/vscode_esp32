
# Lolin ESP32: on-board LED werkt, het OLED display niet: blijft "flat-line'n".
#              Issue: waarschijnlijk probleem met versterking van ADC, signaal
#              is te zwak en hartslag wordt niet goed gedetecteerd.
#
# BvH, 13-10-2019
#

import time
import ssd1306
from machine import Pin, Signal, I2C, ADC #, Timer

# esp32: Vout from hearbeat sensor to ADC ch0 = GPIO4, pin 36.
adc = ADC(Pin(36, Pin.IN), unit=1) # ADC1, ch0
# configureer bereik van 0-3.3 V (3.6 max)
#adc.atten(adc.ATTN_11DB)
adc.atten(adc.ATTN_6DB)

# 12 bits resolutie
adc.width(adc.WIDTH_12BIT)

print(adc.read())
print("ADC klaar voor gebruik")

led = Signal(Pin(5, Pin.OUT), invert=True)

# our display has a resolution of 128 x 64
# our display uses address: 0x78
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

devices = i2c.scan()
print(devices)

MAX_HISTORY = 200
TOTAL_BEATS = 30

HEART = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
]

last_y = 0

def refresh(bpm, beat, v, minima, maxima):
    global last_y

    display.vline(0, 0, 32, 0)
    display.scroll(-1, 0) # Scroll left 1 pixel

    if maxima-minima > 0:
        # Draw beat line.
        y = 32 - int(16 * (v-minima) / (maxima-minima))
        display.line(125, last_y, 126, y, 1)
        last_y = y

    # Clear top text area.
    display.fill_rect(0, 0, 128, 16, 0) # Clear the top text area

    if bpm:
        display.text("%d bpm" % bpm, 12, 0)

    # Draw heart if beating.
    if beat:
        for y, row in enumerate(HEART):
            for x, c in enumerate(row):
                display.pixel(x, y, c)

    display.show()

def calculate_bpm(beats):
    if beats:
        # Truncate beats queue to max
        beats = beats[-TOTAL_BEATS:]
        beat_time = beats[-1] - beats[0]
        if beat_time:
            return (len(beats) / (beat_time)) * 60

def detect():
    # Maintain a log of previous values to 
    # determine min, max and threshold.
    history = []
    beats = []
    beat = False
    bpm = None

    # Clear screen to start.
    display.fill(0)

    while True:
        v = adc.read()
        history.append(v)

        # Get the tail, up to MAX_HISTORY length
        history = history[-MAX_HISTORY:]

        minima, maxima = min(history), max(history)

        threshold_on = (minima + maxima * 3) // 4   # 3/4
        threshold_off = (minima + maxima) // 2      # 1/2

        if v > threshold_on and (not beat):
            beat = True
            led.on()
            beats.append(time.time())
            # Truncate beats queue to max
            #beats = beats[-TOTAL_BEATS:]
            bpm = calculate_bpm(beats)

        if v < threshold_off and beat:
            beat = False
            led.off()

        refresh(bpm, beat, v, minima, maxima)

detect()

