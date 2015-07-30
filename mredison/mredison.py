import mraa
import time
import pyupm_i2clcd as lcd

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Clear
myLcd.clear()

# A kinda blue
myLcd.setColor(0x30, 0x2F, 0xFF)

x = mraa.Gpio(4)
x.dir(mraa.DIR_OUT)

period = 0.15
ledvalue = 1

long_string = ' '*15 + 'Hello Mr. Edison, what\'s going on?' + ' '*15
while(1):
    for i in range(len(long_string) - 16 + 1):
         framebuffer = long_string[i:i+16]
         myLcd.setCursor(0,0)
         myLcd.write(framebuffer)
         print(framebuffer)
         x.write(ledvalue)
         ledvalue = 1 - ledvalue
         time.sleep(period)
