import lib.PicoOled13
import network
import uasyncio as asyncio
import time
from array import array

class Display:

    KEY0_PRESSED_LONG = 'key0_pressed_long'
    KEY0_PRESSED_SHORT = 'key0_pressed_short'
    KEY1_PRESSED_LONG = 'key1_pressed_long'
    KEY1_PRESSED_SHORT = 'key1_pressed_short'

    oled: lib.PicoOled13.OLED_1inch3_SPI
    key_listeners: list
    key0_state: int
    key0_state_ticks: int
    key1_state: int
    key1_state_ticks: int
    show_until_ticks: int
    interval_sec: int
    wlan:bool
    ip_addr: str
    msg_buffer: list
    scroll_pos: int
    on: bool
        
    def __init__(self, interval_sec):
        self.oled =  lib.PicoOled13.get()
        self.oled.clear()
        self.key_listeners = list()
        self.key0_state = 1
        self.key1_state = 1
        self.oled.show()
        self.oled.on()
        time.sleep(0.2)
        self.interval_sec = interval_sec
        self.show_until_ticks = time.ticks_ms() + (interval_sec * 1000)
        self.wlan = False
        self.ip_addr = '0.0.0.0'
        self.msg_buffer = list()
        self.scroll_pos = 0
        self.on = True

    def add_key_listener(self, func):
        self.key_listeners.append(func)
    
    async def scroll_up(self):
        if abs(self.scroll_pos) < len(self.msg_buffer)-4:
            self.scroll_pos -= 1
            await self.__update()

    async def scroll_down(self):
        if self.scroll_pos < 0:
            self.scroll_pos += 1
            await self.__update()

    async def write(self,text):
        self.scroll_pos = 0
        self.msg_buffer.append(text)
        if len(self.msg_buffer) > 100:
            del self.msg_buffer[0]
        await self.__update()

    async def set_wlan(self,wlan):
        self.wlan = wlan
        await self.__update()

    async def set_ip_addr(self,ip_addr):
        self.ip_addr = ip_addr
        await self.__update()

    async def wake_up(self):
        self.show_until_ticks = time.ticks_ms() + (self.interval_sec * 1000)
        self.on = True
        await self.__update()

    async def __update(self):
        if not self.on:
            return
        
        coords = array('h', [127, 0, 127, 63,0,63,0,0])
        self.oled.poly(0,0,coords,0x0000,True)
        curr_line = 3
        curr_scroll_pos = self.scroll_pos
        for msg in reversed(self.msg_buffer):
            if curr_scroll_pos != 0:
                curr_scroll_pos += 1
            else:
                self.oled.text(msg,0,2 + (curr_line*12),0xffff,False)
                if (curr_line == 0):
                    break
                else:
                    curr_line -= 1

        # status
        self.oled.line(0,50,127,50,0xffff)        
        self.oled.text('{0}'.format(self.ip_addr if self.wlan else '...'),0,53,0xffff,False)
        self.oled.show()
        self.oled.on()

    async def run_watchdog(self):        
        while True:
            if (self.oled.is_on == 1) and (time.ticks_ms() > self.show_until_ticks):
                self.on = False
                self.oled.off()

            if self.oled.key0.value() != self.key0_state:
                self.key0_state = self.oled.key0.value()
                if self.key0_state == 0:
                    self.key0_state_ticks = time.ticks_ms()
                elif self.key0_state == 1:
                    curr_ticks = time.ticks_ms()
                    for func in self.key_listeners:
                        await func(self.KEY0_PRESSED_LONG if time.ticks_diff(curr_ticks,self.key0_state_ticks) > 1000 \
                            else self.KEY0_PRESSED_SHORT)
                        
            if self.oled.key1.value() != self.key1_state:
                self.key1_state = self.oled.key1.value()
                if self.key1_state == 0:
                    self.key1_state_ticks = time.ticks_ms()
                elif self.key1_state == 1:
                    curr_ticks = time.ticks_ms()
                    for func in self.key_listeners:
                        await func(self.KEY1_PRESSED_LONG if time.ticks_diff(curr_ticks,self.key1_state_ticks) > 1000 \
                            else self.KEY1_PRESSED_SHORT)

            await asyncio.sleep(0.1)
