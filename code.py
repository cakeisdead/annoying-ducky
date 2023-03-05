"""Main code"""
import time
import os
import digitalio
import adafruit_displayio_ssd1306
import usb_hid
from adafruit_hid.mouse import Mouse
from board import *
import board
import busio as io
import displayio
import terminalio
from adafruit_display_text import label, wrap_text_to_lines
from PicoDucky import PicoDucky
from Oled import oled
from Boto import Boto

## Main
time.sleep(0.5)
boto = Boto()
