#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from roboter import Roboter
from speed import SpeedThread
import papiHilfe 
from portHelper import PortHelper
import inspect 
import sys
from debug import debug, debugLevel
from simple_pid.PID import PID
from reden import Reden
from threading import Thread
from sensorMotorThread import SensorMotorThread
import logging 
from pidThread import PidThread
from arrayFixed import ArrayFixed
from dataDumper import DataDumper
from oszilationDetector import OszilationDetector
import os

os.system("setfont Lat15-TerminusBold32x16")

brick.display.text("test",(30,30))
brick.sound.beep()
while 1:
    wait(19)
sys.exit()


debugLevel=30

r=Roboter(motorLinks=Motor(Port.A),motorRechts=Motor(Port.D))
r.menu()
r.linieFolgenThread(oszilationDetector=OszilationDetector())


self=r
targetColor=self.cs.reflection()

sw=StopWatch()

tu=(47496-46775)/1000
ku=-3.7

kp=.6*ku
ki=1.2*ku/tu
kd=3*ku*tu/40

od=OszilationDetector()
pidThread=PidThread(input=self.cs.reflection,robot=self, oszilationDetector=od)


# pidThread.pidStear.tunings = (-8.340000000000002, -28.70912220309812, -0.6056925)

pidThread.start()

self.drive(0,-30,300)
while not od.oszilating:
    stear=pidThread.stear
    speed=pidThread.speed
    self.drive(speed=0, stearing=stear)
    debug(level=12,showOnBrick=False,msg="init: stear {} speed {}".format(stear,speed))
    wait(5)


pidStear=pidThread.pidStear

tu=(47496-46775)/1000
ku=pidStear.tunings[0]

kp=.6*ku
ki=1.2*ku/tu
kd=3*ku*tu/40

pidStear.tunings = (kp, ki, kd)

while od.oszilating:
    stear=pidStear(self.cs.reflection())
   
    debug("relax: time {} stear: {} tunings {} oszil diff {:4} qouat {:4}".format(sw.time(),stear,pidStear.tunings,od.meanDiff, od.meanQuoat))
    od.add(sw.time,stear)
    self.drive(0,stear)
    wait(5)

while 1:
    stear=pidStear(self.cs.reflection())
   
    debug("drive: time {} stear: {} tunings {} oszil diff {:4} qouat {:4}".format(sw.time(),stear,pidStear.tunings,od.meanDiff, od.meanQuoat))
    od.add(sw.time,stear)
    self.drive(10,stear)
    wait(5)
sys.exit()

r=Roboter()
r.rumFahren()

sys.exit()

r=Roboter()
auswahl=[ (r.linieFolgenThread, "threadded line follow"),(r.linieFolgen, "line follow"), (r.rumFahren, "seaker")]


i=0
while 1:
    if i < 0:
        i = len(auswahl) -1 
    if not i < len(auswahl):
        i=0
    debug(i)
    code, name = auswahl[i]
    Reden.reden(name,False)
    btn = []
    while not any(btn):
        btn = brick.buttons()
        if Button.CENTER in btn:
            Reden.reden(name,False)
            code()
        if Button.LEFT in btn:
            i+=1
            break
        if Button.RIGHT in btn:
            i-=1
            break
        wait(50)