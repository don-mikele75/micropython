# Bibliotheken laden
from machine import Pin
from time import sleep

# Initialisierung von GPIO13 als Ausgang
led = Pin(13, Pin.OUT)

# 10x blinken
for i in range(10):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)