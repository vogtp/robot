from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
import sys 
import os

class Reden():

    @staticmethod
    def reden(msg:text, german=True):
        lang=""
        if german:
            lang="-vde"
        os.system("/usr/bin/espeak -a 200 --stdout '{}' {} > out.wav".format(msg,lang))
        brick.sound.file("out.wav",volume=100)