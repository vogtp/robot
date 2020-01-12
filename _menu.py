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

debugLevel=1

baseSpeed=50
debugLevel=0
r=Roboter()
# 300 -> > 4 (125)
# 200 -> > 6 (33)
# 100 -> > 2 (50)
# 50 -> > 1 (50)
# 30 -> > 0.8 (37)

auswahl=[ (r.linieFolgenThread, "thread line follow"),(r.linieFolgen, "line follow"), (r.rumFahren, "seaker")]


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
