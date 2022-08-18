<p align="center">
  <img src="./img/header.png" alt="duck"/>
</p>

<h1 align="center">annoying-ducky</h1>

Based on dbisu's [Pico-Ducky](https://github.com/dbisu/pico-ducky) project.

## Overview

Inject individual *scripts* or setup a batch of multiple *scripts* to be executed in sequence.

A *script* can be either a **plain text file** or a **ducky script** file.

## Components

+ 1x Raspberry Pi Pico
+ 1x USB Cable
+ 1x OLED display (SSD1306)
+ 4x Push buttons
+ Wires

## Hardware Setup

### OLED Wiring

Connect the following pins from the *OLED display* to the *Raspberry Pi Pico*

| OLED         | Pi Pico      |
|:------------:|:------------:|
| VCC          |  3V3(OUT)    |
| GND          |  GND         |
| SCL          |  GP17        |
| SDA          |  GP16        |

### Push Buttons

On all four *Push Buttons* one pin needs to be connected to the *Pico's* **GND** pin, and then the opposite pin should be connected as followed:

| Push Button  | Pi Pico      |
|:------------:|:------------:|
| UP Button    |  GP13        |
| DOWN Button  |  GP12        |
| SELECT Button|  GP11        |
| CANCEL Button|  GP10        |

## Usage

Power on the device by connecting it to a computer or smartphone and use the **Up** / **Down** buttons to navigate the menu:

### Type

Type an entire plain text file from the Type folder.

### OSX/WIN Ducky

Inject a ducky script, OSX and Windows scripts should be stored in the corresponding folder.

### Stay-Awake

Spams [Win|Command + Tab] to prevent a computer from locking.

### Automatic-Mode

Start the execution of all the scripts in the Playlist right now or the next time the device is plugged in.

### Settings

??????

## Links and Resources

+ [Pico-Ducky](https://github.com/dbisu/pico-ducky)
+ [Using Push Buttons](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/)
+ [RBP Pico Pinout](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#pinout-and-design-files)