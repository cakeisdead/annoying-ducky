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
    WIDTH = 0
    HEIGHT = 0
    BORDER = 5
    
    def __init__(self, wd, hg):
        self.WIDTH = wd
        self.HEIGHT = hg
        displayio.release_displays()
        self.__i2c = io.I2C(self.__scl_pin, self.__sda_pin)
        self.__display_bus = displayio.I2CDisplay(self.__i2c, device_address=self.__device_address)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.__display_bus, width=self.WIDTH, height=self.HEIGHT)
        self.busy_frames('oled_img/duck_one.bmp','oled_img/duck_two.bmp')
    
    def show_menu(self, lines):
        text_area = label.Label(terminalio.FONT, text=lines)
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
    
    def display_message(self, text):
        self.__message = displayio.Group()
        color_bitmap = displayio.Bitmap(self.WIDTH, self.HEIGHT, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.__message.append(bg_sprite)

        # Draw border
        inner_bitmap = displayio.Bitmap(self.WIDTH - self.BORDER * 2, self.HEIGHT - self.BORDER * 2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=self.BORDER, y=self.BORDER
        )
        self.__message.append(inner_sprite)

        # Draw message
        wrapped_text = '\n'.join(wrap_text_to_lines(text, self.WIDTH - (self.BORDER*2)))
        text_area = label.Label(
            terminalio.FONT, text=wrapped_text, color=0xFFFFFF, x=self.BORDER * 3, y=self.BORDER * 3
        )
        self.__message.append(text_area)
        self.display.show(self.__message)

    def bongo(self):
        self.display.show(self.__frame1)
        sleep(0.4)
        self.display.show(self.__frame2)
        sleep(0.4)