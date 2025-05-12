# Bibliotheken laden
from machine import ADC
from time import sleep
import uasyncio as asyncio

# Initialisierung des ADC4
sensor = ADC(1)


def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    machine.soft_reset()

async def run_watchdog():
    while True:
        # Temparatur-Sensor als Dezimalzahl lesen
        value_a = sensor.read_u16()
        print("Wert: ", value_a)
        sleep(0.1)

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.create_task(run_watchdog())
loop.run_forever() 