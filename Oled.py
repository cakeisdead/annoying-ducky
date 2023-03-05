"""Oled capabilities module"""
from time import sleep
import os
import board
from board import *
import displayio
import busio as io
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label, wrap_text_to_lines

class oled:
    """Oled features"""
    __scl_pin = board.GP17
    __sda_pin = board.GP16
    __device_address = 0x3c
    width = 0
    width = 0
    BORDER = 5

    def __init__(self, wd, hg):
        self.width = wd
        self.height = hg
        displayio.release_displays()
        self.__i2c = io.I2C(self.__scl_pin, self.__sda_pin)
        self.__display_bus = displayio.I2CDisplay(self.__i2c, device_address=self.__device_address)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.__display_bus, width=self.width, height=self.height)
        self.busy_frames('oled_img/duck_one.bmp','oled_img/duck_two.bmp')
        self.__message = displayio.Group()

    def show_menu(self, lines):
        """Draw menu active menu lines"""
        text_area = label.Label(terminalio.FONT, text=lines)
        text_area.x = 10
        text_area.y = 20
        self.display.show(text_area)

    def busy_frames(self, bmp1_path, bmp2_path):
        """Define frames for the typing animation"""
        self.__frame1 = displayio.Group()
        first_frame = open(bmp1_path,'rb')
        odb = displayio.OnDiskBitmap(first_frame)
        bongo_one = displayio.TileGrid(odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter()))
        self.__frame1.append(bongo_one)

        self.__frame2 = displayio.Group()
        second_frame = open(bmp2_path,'rb')
        odb = displayio.OnDiskBitmap(second_frame)
        bongo_one = displayio.TileGrid(odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter()))
        self.__frame2.append(bongo_one)

    def display_message(self, text):
        """Display message with a border around the oled display"""  
        color_bitmap = displayio.Bitmap(self.width, self.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.__message.append(bg_sprite)

        # Draw border
        inner_bitmap = displayio.Bitmap(self.width - self.BORDER * 2, self.height - self.BORDER * 2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=self.BORDER, y=self.BORDER
        )
        self.__message.append(inner_sprite)

        # Draw message
        wrapped_text = '\n'.join(wrap_text_to_lines(text, self.width - (self.BORDER*2)))
        text_area = label.Label(
            terminalio.FONT, text=wrapped_text, color=0xFFFFFF, x=self.BORDER * 3, y=self.BORDER * 3
        )
        self.__message.append(text_area)
        self.display.show(self.__message)

    def bongo(self):
        """Start the typing animation"""
        delay_between_frames = 0.4
        self.display.show(self.__frame1)
        sleep(delay_between_frames)
        self.display.show(self.__frame2)
        sleep(delay_between_frames)
