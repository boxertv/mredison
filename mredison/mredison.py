import mraa
import time
import pyupm_i2clcd as lcd
import os

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Clear
myLcd.clear()

# A kinda blue
myLcd.setColor(0x30, 0x2F, 0xFF)

x = mraa.Gpio(4)
x.dir(mraa.DIR_OUT)

period = 0.15
# ledvalue = 1

# filler_text = 'Hello Mr. Edison, what\'s going on?'

# long_string = ' '*15 + filler_text + ' '*15
# while(1):
#     for i in range(len(long_string) - 16 + 1):
#          framebuffer = long_string[i:i+16]
#          myLcd.setCursor(0,0)
#          myLcd.write(framebuffer)
#          print(framebuffer)
#          x.write(ledvalue)
#          ledvalue = 1 - ledvalue
#          time.sleep(period)

class TestBot(irc.bot.SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

	def on_welcome(self, c, e):
		print "connected"
		c.join(self.channel)

	def on_join(self, c, e):
		print "joined"

	def on_pubmsg(self, c, e):
		a = e.arguments[0].split(":", 1)
		user = e.source.split("!", 1)[0]
		message = e.arguments[0]
		print "%s: %s" %(user, message)
		myLcd.setCursor(0,0)
		myLcd.write("%s:" %(user))
		myLcd.setCursor(1,0)
		myLcd.write(message)
		return

def main():
	server = "irc.freenode.net"
	port = 6667
	channel = "#mredison"
	nickname = "mredison3"

	bot = TestBot(channel, nickname, server, port)
	bot.start()

if __name__ == "__main__":
	main()
