import board
from board import *
import displayio
import busio as io
import adafruit_displayio_ssd1306
import os
from time import sleep
import terminalio
from adafruit_display_text import label, wrap_text_to_lines

class oled:
    __scl_pin = board.GP17
    __sda_pin = board.GP16
    __device_address = 0x3c
    
    def __init__(self, wd, hg):
        displayio.release_displays()
        self.__i2c = io.I2C(self.__scl_pin, self.__sda_pin)
        self.__display_bus = displayio.I2CDisplay(self.__i2c, device_address=self.__device_address)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.__display_bus, width=wd, height=hg)
        self.busy_frames('oled_img/duck_one.bmp','oled_img/duck_two.bmp')
    
    def show_menu(self, lines):
        text_area = label.Label(terminalio.FONT, text=lines)
        text_area.x = 10
        text_area.y = 20
        self.display.show(text_area)

    def show_wrapped_line(self, line):
        wrapped_line = '\n'.join(wrap_text_to_lines(str(line), 20))
        text_area = label.Label(terminalio.FONT, text=wrapped_line)
        text_area.x = 10
        text_area.y = 20
        self.display.show(text_area)

    def busy_frames(self, bmp1_path, bmp2_path):
        self.__frame1 = displayio.Group()
        f1 = open(bmp1_path,'rb')
        odb = displayio.OnDiskBitmap(f1)
        bongo_one = displayio.TileGrid(odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter()))
        self.__frame1.append(bongo_one)
        #time.sleep(2)

        self.__frame2 = displayio.Group()
        f2 = open(bmp2_path,'rb')
        odb = displayio.OnDiskBitmap(f2)
        bongo_one = displayio.TileGrid(odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter()))
        self.__frame2.append(bongo_one)
        #time.sleep(2)

    def bongo(self):
        self.display.show(self.__frame1)
        sleep(0.4)
        self.display.show(self.__frame2)
        sleep(0.4)