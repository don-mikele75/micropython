import uasyncio as asyncio
import machine
from time import sleep
import requests
import json
from util.wlan import WlanConnection
        
async def handle_wlan_state_event(is_connected, ip_addr):
    print("WLAN:",is_connected,ip_addr)
    if is_connected:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if (response.status_code == 200):
            joke = json.loads(response.content)
            print()
            print(joke["setup"])
            sleep(2)
            print()
            print(joke["punchline"])

def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    machine.soft_reset()

wlan_connection = WlanConnection()
wlan_connection.add_state_listener(handle_wlan_state_event)

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.create_task(wlan_connection.run_watchdog(5))
loop.run_forever()


