import uasyncio as asyncio
import machine
from time import sleep
import requests
import json
from util.wlan import WlanConnection
from util.webserver import Webserver
        
async def handle_wlan_state_event(is_connected, ip_addr):
    print("WLAN:",is_connected,ip_addr)

def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    machine.soft_reset()

async def handle_config_changed():
    print('config changed')

wlan_connection = WlanConnection()
wlan_connection.add_state_listener(handle_wlan_state_event)

webserver = Webserver()
webserver.add_config_changed_listener(handle_config_changed)

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.create_task(wlan_connection.run_watchdog(5))
loop.create_task(webserver.run_watchdog())
loop.run_forever()


