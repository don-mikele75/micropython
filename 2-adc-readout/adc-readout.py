# Bibliotheken laden
from machine import ADC
from time import sleep

# Initialisierung des ADC4
sensor = ADC(1)

# Wiederholung einleiten (Schleife)
while True:
    # Temparatur-Sensor als Dezimalzahl lesen
    value_a = sensor.read_u16()
    print("Wert: ", value_a)
    sleep(0.1)