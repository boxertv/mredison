import mraa
import time
import pyupm_i2clcd as lcd
import pyupm_buzzer as upmBuzzer
import os

import irc.bot
import irc.strings

import hashlib
import os
import ssl

from multiprocessing import Process, Manager

from datetime import datetime
import pytz

###### Setting up at start

LcdWidth = 16

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.clear()
myLcd.setColor(0x33, 0x33, 0x33)

led = mraa.Gpio(4)
led.dir(mraa.DIR_OUT)

# using GPIO pin 5, has to be a PWM capable pin
buzzer = upmBuzzer.Buzzer(5)
buzzerVolume = 0.25
buzzer.playSound(3000, 1) # arbitrary for set up

###### End setting up

def getColoursFromText(text):
    """Calculate RGB value from first three bytes of the hash value
    of a string (using SHA-256)
    """
    h = hashlib.sha256()
    h.update(text)
    r, g, b = int(h.hexdigest()[0:2], 16), int(h.hexdigest()[2:4], 16), int(h.hexdigest()[4:6], 16)
    return (r, g, b)

def scrolling(display):
    """ Thread to create scrolling effect """
    i = 0
    n = LcdWidth
    while(True):
        try:
            if display['update']:
                display['update'] = False
                display['led'] = True
                i = 0

                author = display['author']
                if len(author) < LcdWidth:
                    showauthor = author + ":"
                else:
                    showauthor = author[0:(LcdWidth-4)] + "...:"

                myLcd.clear()
                colours = getColoursFromText(author)
                myLcd.setColor(*colours)
                myLcd.setCursor(0, 0)
                myLcd.write(showauthor)
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
        except IOError:
            time.sleep(0.1)
            pass

def ledblink(display):
    """Notification LED: blink when it's told to through shared variable
    """
    while(True):
        try:
            if display['led']:
                display['led'] = False
                for i in range(2):
                    led.write(1)
                    time.sleep(0.1)
                    led.write(0)
                    time.sleep(0.1)
                playGTA()
            time.sleep(0.1)
        except IOError:
            time.sleep(0.1)
            pass

notes = {"X1": 471, # 2124Hz
         "X2": 422, # 2370Hz
         "X3": 413, # 2423Hz
         "X4": 389, # 2570Hz
         "X5": 372, # 2690Hz
         "X6": 368, # 2720Hz
         "X7": 349} # 2865Hz
def playGTA():
    tempo = 60 * 1000
    pager = [("X7", 5), ("X7", 5), ("X7", 1), (" ", 4),
             ("X4", 2), ("X7", 2), ("X2", 2), ("X7", 2), (" ", 2),
             ("X4", 2), ("X7", 5), (" ", 4),
             ("X7", 2), (" ", 2),
             ("X7", 5), ("X7", 1), (" ", 1),
             ("X4", 5), ("X4", 5), ("X4", 1), (" ", 1),
             ("X3", 5), ("X7", 5)]
    playMelody(pager, tempo)

def playMelody(melody, tempo):
    buzzer.setVolume(buzzerVolume)
    for m in melody:
        note, beat = m
        if note == " ":
            buzzer.setVolume(0.0)
            buzzer.playSound(3000, beat * tempo)
            buzzer.setVolume(buzzerVolume)
        else:
            buzzer.playSound(notes[note], beat * tempo)
        # add a bit of trailing break
        buzzer.setVolume(0.0)
        buzzer.playSound(3000, int(0.1 * tempo))
        buzzer.setVolume(buzzerVolume)

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6697, timezone='UTC'):
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
        self.timezone = pytz.timezone(timezone)

        ## Make sure not to choke on non-Unicode characters
        ## The default DecodingLineBuffer can crash with UnicodeDecodeError
        self.connection.buffer_class = irc.buffer.LenientDecodingLineBuffer

        # Display threads and variables setup
        self.manager = Manager()
        self.display = self.manager.dict()
        self.display['author'] = ''
        self.display['text'] = ''
        self.display['update'] = False
        self.display['led'] = False
        showdisplay = Process(target=scrolling, args=(self.display,))
        showdisplay.start()
        blink = Process(target=ledblink, args=(self.display,))
        blink.start()

    def on_nicknameinuse(self, c, e):
        """Handle nickname collision by adjusting the base name
        """
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print "connected"
        c.join(self.channel)

    def on_join(self, c, e):
        if self._get_user(e) == c.get_nickname():
            print "joined channel"

    def on_pubmsg(self, c, e):
        """Handle message on the channel to process and display
        """
        a = e.arguments[0].split(":", 1)
        user = e.source.split("!", 1)[0].encode('ascii', 'replace')
        message = e.arguments[0].encode('ascii', 'replace')
        print "%s: %s" %(user, message)

        utctime = datetime.utcnow()
        utctime = utctime.replace(tzinfo=pytz.utc)
        messagetime = utctime.astimezone(self.timezone).strftime("%H:%M")

        self.display['author'] = user
        self.display['text'] = messagetime + " " + message
        self.display['update'] = True
        return

    def _get_user(self, e):
        """ Helper function: get user from the event """
        return e.source.split("!", 1)[0].encode('ascii', 'replace')

def main():
    """ Starting the IRC bot with the proper environmental variables
    """
    server = os.getenv('SERVER', "irc.freenet.net")
    port = int(os.getenv('PORT', 6697))
    channel = os.getenv('CHANNEL', "#mredison")
    nickname = os.getenv('NICK', "mredison")
    bottz = os.getenv('TIMEZONE', "UTC")

    bot = TestBot(channel, nickname, server, port, bottz)
    bot.start()

if __name__ == "__main__":
    main()
