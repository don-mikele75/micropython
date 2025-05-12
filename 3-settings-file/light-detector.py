import uasyncio as asyncio
import machine
from util.ldr import LightDetector
from util.settings import Settings

async def handle_value_event(value):
    pass
    # print(value)

async def handle_alarm_event(is_alarm):
    if is_alarm:
        print("* ALARM")
    else:
        print(".. all clear")

def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    machine.soft_reset()

settings = Settings.load()
print("On LDR value:", settings.led_on_minimum_ldr)
settings.save()

light_detector = LightDetector()
light_detector.add_alarm_listener(handle_alarm_event)
light_detector.add_value_listeners(handle_value_event)

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.create_task(light_detector.run_watchdog())
loop.run_forever()