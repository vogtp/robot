#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from roboter import Roboter
from speed import Speed
import papiHilfe 
from portHelper import PortHelper
import inspect 
import sys
from debug import debug

debug("*****  DEBUG *******")

us = PortHelper.getSensor(UltrasonicSensor)

baseSpeed=50
roboter=Roboter(speed=baseSpeed)


speed = Speed(roboter=roboter)
speed.start()




while 1:
    
    roboter.drive()
    if speed():
        brick.sound.beep()
        roboter.ausweichen()

    if us and us.distance() < 50:
        roboter.stop()
        brick.sound.file(SoundFile.DETECTED)
        roboter.ausweichen()

    btns = brick.buttons()
    while any(btns):
        roboter.stop()
        if Button.CENTER in btns:
            roboter.steuer = 0
            roboter.speed = baseSpeed
        if Button.UP in btns:
            roboter.speed = roboter.speed + 1
        if Button.DOWN in btns:
            roboter.speed = roboter.speed - 1
        if Button.RIGHT in btns:
            roboter.steuer = roboter.steuer + 1
        if Button.LEFT in btns:
            roboter.steuer = roboter.steuer - 1
        
        brick.display.clear()
        brick.display.text("Speed {}".format(roboter.speed), (20,60))
        brick.display.text("Steuer {}".format(roboter.steuer))
        wait(100)
        btns = brick.buttons()

    roboter.drive()
        
    wait(10)
