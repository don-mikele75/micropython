import uasyncio as asyncio
import machine
from time import sleep
import requests
import json
from util.wlan import WlanConnection
from util.display import Display
        
async def handle_wlan_state_event(is_connected, ip_addr):
    await display.set_wlan(is_connected)
    await display.set_ip_addr(ip_addr)

def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    machine.soft_reset()

async def handle_display_key_event(key_event):
    await display.wake_up()
    if key_event == display.KEY0_PRESSED_SHORT:
        await display.scroll_up()
    elif key_event == display.KEY1_PRESSED_SHORT:
        await display.scroll_down()
    elif key_event == display.KEY0_PRESSED_LONG:
        await display.write("KEY0_PRESSED_LONG")
    elif key_event == display.KEY1_PRESSED_LONG:
        await display.write("KEY1_PRESSED_LONG")

display = Display(5)
display.add_key_listener(handle_display_key_event)

wlan_connection = WlanConnection()
wlan_connection.add_state_listener(handle_wlan_state_event)

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.create_task(display.run_watchdog())
loop.create_task(wlan_connection.run_watchdog(5))
loop.run_forever()
