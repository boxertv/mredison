"""
Play melody with buzzer
"""
import mraa
import time
import datetime

# Save shortcuts to these functions to speed things up
now = datetime.datetime.now
timedelta = datetime.timedelta
sleep = time.sleep

class Melody:
    """ Melody player tool
    """
    ## Original GTA notes
    # "X1": 235, # 2124Hz
    # "X2": 211, # 2370Hz
    # "X3": 206, # 2423Hz
    # "X4": 195, # 2570Hz
    # "X5": 186, # 2690Hz
    # "X6": 184, # 2720Hz
    # "X7": 175, # 2865Hz
    notes = {"c": 1915,
             "d": 1700,
             "e": 1519,
             "f": 1432,
             "g": 1275,
             "a": 1136,
             "b": 1014,
             "C": 956,
             "D7": 212,
             "D#7": 200,
             "E7": 189,
             "F7": 176,
             "X1": 250,
             "X2": 230,
             "X3": 206,
             "X4": 195,
             "X5": 195,
             "X6": 175,
             "X7": 155}

    def __init__(self, buzzerPin):
        self.buzz = mraa.Gpio(buzzerPin)
        self.buzz.dir(mraa.DIR_OUT)

    def playTone(self, tone, duration):
        """play a tone

        tone: time high in microseconds (us)
        duration: tone duration in milliseconds (ms)

        Eg:
        note    frequency    period(us) timehigh(us)
        a       440 Hz       2272       1136
        """
        dt = timedelta(microseconds=int(duration*1e3))
        dtone = timedelta(microseconds=tone)
        finish = now() + dt
        while now() < finish:
            tonefinish = now() + dtone
            self.buzz.write(1)
            while now() < tonefinish:
                pass
            tonefinish = now() + dtone
            self.buzz.write(0)
            while now() < tonefinish:
                pass

             # "X1": 235, # 2124Hz
             # "X2": 211, # 2370Hz
             # "X3": 206, # 2423Hz
             # "X4": 195, # 2570Hz
             # "X5": 186, # 2690Hz
             # "X6": 184, # 2720Hz
             # "X7": 175, # 2865Hz
    def playNote(self, note, duration):
        """ Play a single note
        """
        if note in self.notes:
            self.playTone(self.notes[note], duration)
        else:
            # Have a pause
            dt = timedelta(microseconds=int(duration*1e3))
            finish = now() + dt
            while now() < finish:
                pass

    def playGTA(self):
        """ Play a modified version of the GTA III pager sound
        """
        tempo = 60
        ### Original transcript
        # pager = [("X7", 5), ("X7", 5), ("X7", 1), (" ", 4),
        #          ("X4", 2), ("X7", 2), ("X2", 2), ("X7", 2), (" ", 2),
        #          ("X4", 2), ("X7", 5), (" ", 4),
        #          ("X7", 2), (" ", 2),
        #          ("X7", 5), ("X7", 1), (" ", 1),
        #          ("X6", 5), ("X6", 5), ("X6", 1), (" ", 1),
        #          ("X3", 5), ("X7", 5),
        # ]
        ### Modified transscript
        pager = [("X7", 5), ("X7", 5), ("X7", 1), (" ", 4),
                 ("X4", 2), ("X7", 2), ("X2", 2), ("X7", 2), (" ", 2),
                 ("X4", 2), ("X7", 5), (" ", 4),
                 ("X7", 2), (" ", 2),
                 ("X7", 5), ("X7", 1), (" ", 1),
                 ("X4", 5), ("X4", 5), ("X4", 1), (" ", 1),
                 ("X3", 5), ("X7", 5)]
        for m in pager:
            note, beat = m
            self.playNote(note, beat * tempo)
            sleep(tempo/2/1000)

if __name__ == "__main__":
    melody = Melody(2)
    melody.playGTA()
