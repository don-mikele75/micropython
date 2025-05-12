# Bibliotheken laden
from machine import ADC
from time import sleep

# Initialisierung des ADC4
sensor = ADC(1)

# Wiederholung einleiten (Schleife)
while True:
    # Temparatur-Sensor als Dezimalzahl lesen
    value_a = sensor.read_u16()
    print("Dezimalzahl: ", value_a)
    # 0,2 Sekunden warten
    sleep(0.2)