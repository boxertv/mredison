import mraa
import time
import pyupm_i2clcd as lcd
import os

import irc.bot
import irc.strings

import hashlib
import os
import ssl

from multiprocessing import Process, Manager


myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
LcdWidth = 16

# Clear
myLcd.clear()

myLcd.setColor(0x33, 0x33, 0x33)

led = mraa.Gpio(4)
led.dir(mraa.DIR_OUT)

def scrolling(display):
    """ Thread to create scrolling effect """
    lasttime = 0.0
    i = 0
    n = LcdWidth
    while(True):
        if display['time'] > lasttime:
            lasttime = display['time']
            i = 0
        else:
            text = display['text']
            text_length = len(text)
            if (text_length <= n):
                showtext = text + " "*(n - text_length)
                # print(showtext)
                myLcd.setCursor(1, 0)
                myLcd.write(showtext)
            else:
                showtext = text + " "*(n-1)
                # print(showtext[i:i+n])
                myLcd.setCursor(1, 0)
                myLcd.write(showtext[i:i+n])
                if (i == 0):
                    time.sleep(1)
                i += 1
                if (i > text_length):
                    i = 0
        time.sleep(0.2)

def ledblink(display):
    while(True):
        if display.led:
            display.led = False
            for i in range(3):
                led.write(1)
                time.sleep(0.2)
                led.write(0)
                time.sleep(0.2)
        sleep(0.1)

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6697):
        connect_params = {}
        connect_params['connect_factory'] = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(self,
                                            [(server, port)],
                                            nickname,
                                            nickname,
                                            30,
                                            **connect_params
                                           )
        self.channel = channel
        self.manager = Manager()
        self.display = self.manager.dict()
        self.display['text'] = ''
        self.display['time'] = 0
        self.display['led'] = False
        showdisplay = Process(target=scrolling, args=(self.display,))
        showdisplay.start()
        blink = Process(target=ledblink, args=(self.display,))
        blink.start()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print "connected"
        c.join(self.channel)

    def on_join(self, c, e):
        if self._get_user(e) == c.get_nickname():
            print "joined channel"

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        user = e.source.split("!", 1)[0].encode('ascii', 'replace')
        message = e.arguments[0].encode('ascii', 'replace')
        h = hashlib.sha256()
        h.update(user)
        r, g, b = int(h.hexdigest()[0:2], 16), int(h.hexdigest()[2:4], 16), int(h.hexdigest()[4:6], 16)
        print "%s: %s" %(user, message)

        if len(user) < LcdWidth:
            showuser = user + ":"
        else:
            showuser = user[0:(LcdWidth-4)] + "...:"

        myLcd.clear()
        myLcd.setColor(r, g, b)
        myLcd.setCursor(0, 0)
        myLcd.write(showuser)
        self.display['text'] = message
        self.display['time'] = time.time()
        return

    def on_ctcp(self, c, e):
        """Default handler for ctcp events.

        Replies to VERSION and PING requests and relays DCC requests
        to the on_dccchat method.
        """
        nick = e.source.nick
        if e.arguments[0] == "VERSION":
            c.ctcp_reply(nick, "VERSION " + self.get_version())
        elif e.arguments[0] == "PING":
            print "PING"
            if len(e.arguments) > 1:
                c.ctcp_reply(nick, "PING " + e.arguments[1])
        elif e.arguments[0] == "DCC" and e.arguments[1].split(" ", 1)[0] == "CHAT":
            self.on_dccchat(c, e)

    def _get_user(self, e):
        """ Helper function: get user from the event """
        return e.source.split("!", 1)[0].encode('ascii', 'replace')

def main():
    server = os.getenv('SERVER', "irc.freenet.net")
    port = int(os.getenv('PORT', 6697))
    channel = os.getenv('CHANNEL', "#mredison")
    nickname = os.getenv('NICK', "mredison")

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
