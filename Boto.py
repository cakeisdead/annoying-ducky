"""BOTO: based on dbisu's pico-ducky + an oled display"""
import json
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
from PicoDucky import PicoDucky
from Oled import oled

class Boto():
    """Main class"""
    settings = {}
    playlist = []
    setting_value = False

    menus = {
                'active':'main',
                'main':['Type','OSX Ducky','WIN Ducky','Stay-Awake','Automatic-Mode','Settings'],
                'type':[f for f in os.listdir('text_files') if not f.startswith('.')],
                'osx_ducky':[f for f in os.listdir('osx_ducky') if not f.startswith('.')],
                'script_actions':['Execute','Add to Playlist'],
                'auto-mode':['Start','Playlist','Clear Playlist'], 
                'settings':['Set Delay','Auto-Mode'],
                'playlist':[]
    }

    active_script = {
        'name':'',
        'path':'',
        'type':''
    }

    def __init__(self):
        self.load_settings()
        # Initialize Oled 
        get_oled_props = lambda x: self.settings["oled"][0][x]
        width, height = map(get_oled_props, ('width','height'))
        self.oled = oled(width, height)  

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
                if self.menus['active'] == 'script_actions':
                    self.menus['active'] = self.active_script['type']
                    self.active_script.clear()
                else:
                    self.menus['active'] = 'main'
                self.oled.show_menu(self.visible_menu())
                time.sleep(0.5)

    def set_new_delay(self):
        """Set the delay time between each script"""
        time.sleep(0.5)
        self.setting_value = True
        new_delay_value = self.settings['default_delay']
        self.oled.display_message(f'Default Delay: \n {new_delay_value}')

        while self.setting_value:

            if self.select.value or self.cancel.value:
                self.setting_value = False
            elif self.up.value:
                new_delay_value += 50
            elif self.down.value:
                new_delay_value -= 50

            self.oled.display_message(f'Default Delay: \n {new_delay_value}')

        if new_delay_value != self.settings['default_delay']:
            self.settings['default_delay'] = new_delay_value
            self.save_settings()

    def load_settings(self):
        """Load existing settings"""
        with open('settings.json', 'r', encoding="utf-8") as config_file:
            self.settings = json.load(config_file)

    def save_settings(self):
        """Save current settings into json file"""
        try:
            with open('settings.json', 'w', encoding="utf-8") as config_file:
                json.dump(self.settings, config_file)
                self.oled.display_message('New settings saved :)')
        except:
            self.oled.display_message('New settings could not be saved :(')


    def visible_menu(self):
        """Define the visible menu lines"""
        try:
            lines = '  ' + self.menus[self.menus['active']][0] + '\n'
            lines += '> ' + self.menus[self.menus['active']][1] + '\n'
            lines += '  ' + self.menus[self.menus['active']][2] + '\n'
        except:
            pass
        return lines

    def save_playlist_changes(self):
        """Save current playlist into a json file"""
        with open('playlist.json','w',encoding='utf-8') as output:
            json.dump(self.playlist, output)

    def add_to_playlist(self, script):
        """Add single script to the playlist"""
        self.playlist.append(script)
        self.save_playlist_changes()

    def clear_playlist(self):
        """Remove all scripts from the playlist""" 
        self.playlist = []
        self.save_playlist_changes()

    def load_playlist(self):
        """Load the list of scripts"""
        with open('playlist.json','r',encoding='utf-8') as playlist:
            self.playlist = json.load(playlist)

        if self.playlist != []:
            self.menus['playlist'] = [str(i) + " " + f['name'] for i, f in enumerate(self.playlist, 1)]
            self.menus['active'] = 'playlist'
        else:
            self.oled.display_message('Playlist is empty')
            time.sleep(1)
            self.menus['active'] = 'auto-mode'

    def menu_nav(self, active_menu, direction):
        """OLED navigation function, list is updated depending on the direction"""
        if direction=='up' and not self.setting_value:
            self.menus[active_menu].append(self.menus[active_menu].pop(0))

        if direction=='down' and not self.setting_value:
            self.menus[active_menu].insert(0,self.menus[active_menu].pop())

        self.oled.show_menu(self.visible_menu())

    def execute_single(self, active_script):
        """Executes a single script"""
        path, name, type = map(active_script.get, ('path', 'name', 'type'))
        k = PicoDucky(path + name, self.settings['default_delay'])
        if type == 'type':
            result = k.plain_text_type(self.oled, self.cancel)
        else:
            result = k.run_script(self.oled, self.cancel)
        self.menus['active'] = type
        self.oled.show_menu(self.visible_menu()) 
        time.sleep(0.5)
        return result

    def set_active(self, name, type):
        """Set properties of the script to be executed"""
        self.active_script['name'] = name
        self.active_script['path'] = 'text_files/' if type == 'type' else 'osx_ducky/'
        self.active_script['type'] = type

    def batch_executor(self, playlist):
        """Executes a list of scripts sequentially"""
        script_ind = 1
        for script in playlist:
            self.set_active(script['name'], script['type'])
            batch_result = self.execute_single(script)
            script_ind += 1
            if batch_result == "CANCELLED":
                break

    def select_option(self, menu):
        """Actions for the select button"""
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

        if self.menus[menu][1] == 'Automatic-Mode':
            self.menus['active'] = 'auto-mode'
            self.oled.show_menu(self.visible_menu())
            time.sleep(0.5)

        if self.menus[menu][1] == 'Settings':
            self.menus['active'] = 'settings'
            self.oled.show_menu(self.visible_menu())
            time.sleep(0.5)

        if menu == 'type' or menu == 'osx_ducky':
            self.set_active(self.menus[menu][1], menu)
            self.menus['active'] = 'script_actions'
            self.oled.show_menu(self.visible_menu()) 
            time.sleep(0.5)

        if self.menus[menu][1] == 'Execute':
            self.execute_single(self.active_script)

        if self.menus[menu][1] == 'Add to Playlist':
            self.add_to_playlist(self.active_script.copy())
            self.oled.display_message('Added to Playlist')
            time.sleep(1.5)
            self.oled.show_menu(self.visible_menu()) 

        if self.menus[menu][1] == 'Clear Playlist':
            self.clear_playlist()
            self.oled.display_message('Playlist cleared')
            time.sleep(1.5)
            self.oled.show_menu(self.visible_menu())

        if self.menus[menu][1] == 'Start':
            self.batch_executor(self.playlist)

        if self.menus[menu][1] == 'Playlist':
            self.load_playlist()
            self.oled.show_menu(self.visible_menu())
            time.sleep(0.5)

        if self.menus[menu][1] == 'Clear Playlist':
            self.playlist.clear()
            self.menus['active'] = 'main'
            self.oled.show_menu(self.visible_menu())
            time.sleep(0.5)

        if self.menus[menu][1] == 'Set Delay':
            self.set_new_delay()
            time.sleep(1)
