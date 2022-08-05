### PicoDucky
# https://github.com/dbisu/pico-ducky
# License : GPLv2.0
# copyright (c) 2021  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)

import usb_hid
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_la import KeyboardLayout
from keycode_win_la import Keycode
from time import sleep
import digitalio
from board import *

class PicoDucky:
    __default_delay = 50
    __led = digitalio.DigitalInOut(LED)
    __duckyCommands = {
        'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
        'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
        'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
        'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
        'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
        'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
        'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
        'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
        'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
        'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
        'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
        'BACKSPACE': Keycode.BACKSPACE, 'DELETE': Keycode.DELETE,
        'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
        'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
        'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
        'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
        'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
        'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
        'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
        'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
        'F12': Keycode.F12,
    }

    def __init__(self, file_path="", file_type = ""):
        self.__file_path = file_path
        self.__kbd = Keyboard(usb_hid.devices)
        self.__layout = KeyboardLayout(self.__kbd)
        self.__led.direction = digitalio.Direction.OUTPUT
    
    def convertLine(self, line):
        newline = []
        # print(line)
        # loop on each key - the filter removes empty values
        for key in filter(None, line.split(" ")):
            key = key.upper()
            # find the keycode for the command in the list
            command_keycode = self.__duckyCommands.get(key, None)
            if command_keycode is not None:
                # if it exists in the list, use it
                newline.append(command_keycode)
            elif hasattr(Keycode, key):
                # if it's in the Keycode module, use it (allows any valid keycode)
                newline.append(getattr(Keycode, key))
            else:
                # if it's not a known key name, show the error for diagnosis
                print(f"Unknown key: <{key}>")
        # print(newline)
        return newline

    def runScriptLine(self, line):
        for k in line:
            self.__kbd.press(k)
        self.__kbd.release_all()

    def sendString(self, line):
        self.__layout.write(line)

    def parseLine(self, line):
        if(line[0:3] == "REM"):
            # ignore ducky script comments
            pass
        elif(line[0:5] == "DELAY"):
            sleep(float(line[6:])/1000)
        elif(line[0:6] == "STRING"):
            self.sendString(line[7:])
        elif(line[0:5] == "PRINT"):
            print("[SCRIPT]: " + line[6:])
        elif(line[0:6] == "IMPORT"):
            self.runScript(line[7:])
        elif(line[0:13] == "DEFAULT_DELAY"):
            self.__default_delay = int(line[14:]) * 10
        elif(line[0:12] == "DEFAULTDELAY"):
            self.__default_delay = int(line[13:]) * 10
        elif(line[0:3] == "LED"):
            self.__led.value = not self.__led.value
        else:
            newScriptLine = self.convertLine(line)
            self.runScriptLine(newScriptLine)

    def run_script(self):
        duckyScriptPath = self.__file_path
        f = open(duckyScriptPath,"r",encoding='utf-8')
        previousLine = ""
        for line in f: 
            line = line.rstrip()
            if(line[0:6] == "REPEAT"):
                for i in range(int(line[7:])):
                    #repeat the last command
                    self.parseLine(previousLine)
                    sleep(float(self.__default_delay)/1000)
            else:
                self.parseLine(line)
                previousLine = line
            sleep(float(self.__default_delay)/1000)
    def plain_text_type(self, oled):
        sleep(3)
        self.__led.value = True
        file_path = self.__file_path
        with open(file_path,"r",encoding='utf-8') as f:
            for line in f:
                    #oled.show_wrapped_line(line)
                    oled.bongo()
                    self.parseLine('STRING ' + line)
                    self.parseLine('DELAY 250')
        self.__led.value = False
    def keep_alive(self, oled):
        win = self.__duckyCommands.get('WINDOWS', None)
        tab = self.__duckyCommands.get('TAB', None)
        self.__kbd.press(win, tab)
        self.__kbd.release_all()
        oled.bongo()