import network
import uasyncio as asyncio
from time import sleep

class WlanConnection:

    WLAN_SSID = "dev"
    WLAN_PW = ""
    state_listeners: list
    log_async: function

    def __init__(self):
        self.state_listeners = list()
        network.country("DE")
        network.hostname("pico-mwa")
        
    def add_state_listener(self, func):
        self.state_listeners.append(func)

    async def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.WLAN_SSID, self.WLAN_PW)
        print('WLAN - connecting...',self.WLAN_SSID)
        while not wlan.isconnected() and wlan.status() >= 0:
            await asyncio.sleep(1)
        if wlan.isconnected():
            print('WLAN - connected: {0}'.format(wlan.ifconfig()[0]))
            for func in self.state_listeners:
                await func(True,wlan.ifconfig()[0])

    async def run_watchdog(self,interval_sec):
        print('WLAN daemon...')
        while True:
            wlan = network.WLAN(network.STA_IF)
            if not wlan.isconnected():
                for func in self.state_listeners:
                    await func(False,'')
                await self.connect()
            await asyncio.sleep(interval_sec)
