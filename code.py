import time
import board
import touchio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import neopixel

consumer_control = ConsumerControl(usb_hid.devices)

touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, auto_write=False, brightness=0.05)

def pixel_wipe(colour, clockwise=True, duration=0.5):

    start = time.monotonic()
    increment = -1
    if not clockwise:
        increment = 1
        
    while time.monotonic() < start + duration:
        i = 0
        for _ in range(len(pixels)):
            elapsed_percent = (time.monotonic() - start)/duration
            pixels[i] = (colour[0]*elapsed_percent, colour[1]*elapsed_percent, colour[2]*elapsed_percent)
            time.sleep(0.05)
            pixels.show()
            
            i += increment
            
    pixels.fill((0,0,0))
    pixels.show()
    

while True:

    if touch1.value:
        while touch1.value:
            time.sleep(0.1)
        consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        pixel_wipe((0,255,0), clockwise=False)
        
    if touch2.value:
        while touch2.value:
            time.sleep(0.1)
        consumer_control.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        pixel_wipe((255,0,0))