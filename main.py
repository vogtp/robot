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

debugLevel=30

r=Roboter(motorLinks=Motor(Port.A),motorRechts=Motor(Port.D))
r.linieFolgen()

sys.exit()

self=r
targetColor=self.cs.reflection()

sw=StopWatch()

tu=(11271-10498)/1000
ku=-10.4

kp=.6*ku
ki=1.2*ku/tu
kd=3*ku*tu/40

pidStear = PID(Kp=-2.5,Ki=-0.,Kd=0.1, setpoint=targetColor, output_limits=(-120,120))
#pidStear = PID(Kp=kp,Ki=ki,Kd=kd, setpoint=targetColor, output_limits=(-160,160))
debug("tunings {} - ku {} tu {}".format(pidStear.tunings,ku,tu))

while 1:
    #tunings = pidStear.tunings
    #pidStear.tunings = ( tunings[0] - 0.1, tunings[1], tunings[2])
    
    #debug("time {} stear: {} tunings {}".format(sw.time(),stear,tunings))
    self.drive(50,pidStear(self.cs.reflection()))
    #wait(10)



sys.exit()

r=Roboter()
r.rumFahren()

sys.exit()

r=Roboter()
auswahl=[ (r.linieFolgen, "line follow"), (r.rumFahren, "seaker")]


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