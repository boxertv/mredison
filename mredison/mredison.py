import mraa
import time
import pyupm_i2clcd as lcd

myLcd = lcd.Jhd1313m1(6, 0x3E, 0x62)

# Clear
myLcd.clear()

# Green
myLcd.setColor(255, 255, 0)

# Zero the cursor
myLcd.setCursor(0,0)

# Print it.
myLcd.write("What's up?");

x = mraa.Gpio(7)
x.dir(mraa.DIR_OUT)

while True:
    x.write(1)
    time.sleep(0.2)
    x.write(0)
    time.sleep(0.2)
