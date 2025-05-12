import machine
import uasyncio as asyncio
from util.settings import Settings
import time

class LightDetector:

    settings: Settings
    ldr: machine.ADC 
    value: int
    alarm_listeners: list
    value_listeners: list
    log_async: function

    def __init__(self):
        self.settings = Settings.load()
        self.ldr = machine.ADC(1)  # Initialize an ADC object for pin 27
        self.value = 0
        self.alarm_listeners = list()
        self.value_listeners = list()

    def add_alarm_listener(self, func):
        self.alarm_listeners.append(func)

    def add_value_listeners(self, func):
        self.value_listeners.append(func)

    def reload_config(self):
        self.settings = Settings.load()       
        
    async def run_watchdog(self):
        print('LDR daemon started...')
        state = False
        stateTrueTicks = 0

        while True:       
            self.value = self.ldr.read_u16()  # type: ignore # Read the LDR value and convert it to a 16-bit unsigned integer
            for func in self.value_listeners:
                await func(self.value)
            await asyncio.sleep_ms(self.settings.ldr_polling_ms)
            if (self.value < self.settings.led_on_minimum_ldr):
                if (state == False):                
                    state = True
                    for func in self.alarm_listeners:
                        await func(state)
                stateTrueTicks = time.ticks_ms()
                
            if (time.ticks_diff(time.ticks_ms(),stateTrueTicks) >= (self.settings.led_on_timeout_sec*1000)) and (self.value > self.settings.led_on_minimum_ldr):
                if (state == True):
                    state = False
                    for func in self.alarm_listeners:
                        await func(state)
                stateTrueTicks = 0
