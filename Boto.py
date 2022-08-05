from PicoDucky import PicoDucky
from Oled import oled
import digitalio
import adafruit_displayio_ssd1306
import usb_hid
from adafruit_hid.mouse import Mouse
from board import *
import board
import os

import busio as io
import time
import displayio
import terminalio
from adafruit_display_text import label, wrap_text_to_lines

class Boto():
    menus = {
                'active':'main',
                'main':['Type','OSX Ducky','Win Ducky','Stay-Awake'],
                'type':[f for f in os.listdir('text_files') if not f.startswith('.')],
                'osx_ducky':[f for f in os.listdir('osx_ducky') if not f.startswith('.')]
                }
    
    def __init__(self):
        # Initialize Oled 
        self.oled = oled(128, 64)    
        
        # Initialize Buttons
        self.select = digitalio.DigitalInOut(board.GP11)
        self.select.switch_to_input(pull=digitalio.Pull.DOWN)

        self.cancel = digitalio.DigitalInOut(board.GP10)
        self.cancel.switch_to_input(pull=digitalio.Pull.DOWN)

        self.down = digitalio.DigitalInOut(board.GP12)
        self.down.switch_to_input(pull=digitalio.Pull.DOWN)

        self.up = digitalio.DigitalInOut(board.GP13)
        self.up.switch_to_input(pull=digitalio.Pull.DOWN)

        while True:
            if self.down.value:
                self.menu_nav(self.menus['active'],'down')
                time.sleep(0.2)
            if self.up.value:
                self.menu_nav(self.menus['active'],'up')
                time.sleep(0.2)
            if self.select.value:
                self.select_option(self.menus['active'])
            if self.cancel.value:
                self.menus['active'] = 'main'
                self.oled.show_menu(self.visible_menu())
    
    def visible_menu(self):
        lines = '  ' + self.menus[self.menus['active']][0] + '\n'
        lines += '> ' + self.menus[self.menus['active']][1] + '\n'
        lines += '  ' + self.menus[self.menus['active']][2] + '\n'
        return lines
    
    def menu_nav(self, active_menu, direction):
        if direction=='up':
            self.menus[active_menu].append(self.menus[active_menu].pop(0))
        if direction=='down':
            self.menus[active_menu].insert(0,self.menus[active_menu].pop())
        
        self.oled.show_menu(self.visible_menu())     

    def select_option(self, menu):
        if self.menus[menu][1] == 'Type':
            self.menus['active'] = 'type'
            self.oled.show_menu(self.visible_menu()) 
            time.sleep(0.5)
        if self.menus[menu][1] == 'OSX Ducky':
            self.menus['active'] = 'osx_ducky'
            self.oled.show_menu(self.visible_menu())
            time.sleep(0.5)
        if self.menus[menu][1] == 'Stay-Awake':
            k = PicoDucky()
            running = True
            while running:
                k.keep_alive(self.oled)
                if self.cancel.value:
                    running = False
        if menu == 'type':
            k = PicoDucky(f'text_files/{self.menus[menu][1]}')
            k.plain_text_type(self.oled)
            self.menus['active'] = 'main'
        if menu == 'osx_ducky':
            ducky = PicoDucky(f'osx_ducky/{self.menus[menu][1]}')
            ducky.run_script()
            self.menus['active'] = 'main'