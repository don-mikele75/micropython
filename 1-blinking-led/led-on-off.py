# Bibliotheken laden
from machine import Pin
from time import sleep

# Initialisierung von GPIO13 als Ausgang
led = Pin(13, Pin.OUT)

# LED einschalten
led.on()

# 5 Sekunden warten
sleep(5)

# LED ausschalten
led.off()