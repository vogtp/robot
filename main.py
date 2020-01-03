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
from simple_pid.PID import PID
from reden import Reden

baseSpeed=50

r=Roboter()


def calibieren():
    cs = PortHelper.getSensor(ColorSensor)
    
    Reden.reden("Linie")
    while not any(brick.buttons()):
        wait(10)
    linie=cs.reflection()
    Reden.reden("Linie {}".format(linie) )
    print("Linie {}".format(linie) )
    Reden.reden("Hintergrund")
    while not any(brick.buttons()):
        wait(10)
    hintergrund=cs.reflection()
    Reden.reden("Hintergrund {}".format(hintergrund))
    print("Hintergrund {}".format(hintergrund))
    Reden.reden("Start")
    while not any(brick.buttons()):
        wait(10)
    targetColor=cs.reflection()
    Reden.reden("Start {}".format(targetColor))
    print("Start {}".format(targetColor))

#calibieren()
#sys.exit()

def lineFollower():
    cs = PortHelper.getSensor(ColorSensor)
    print("ambient {} color {} reflection {} rgb {}".format(cs.ambient(),cs.color(),cs.reflection(),cs.rgb()))
    motor_links=Motor(Port.D)
    motor_rechts=Motor(Port.B)
    #papiHilfe.wartenAmAnfang()
    targetColor=cs.reflection()
    Reden.reden("Farbe {}".format(targetColor))

    #pid = PID(10,5,2., targetColor, output_limits=(-190,190))
    pidStear = PID(Kp=-5,Ki=-1.0,Kd=.0, setpoint=targetColor, output_limits=(-100,100))
   # pidSpeed = PID(3,1,3, 20, output_limits=(20,100))

    baseSpeed = 50

   # motor_rechts.dc(50)
   # motor_links.dc(50)
    motor_links.run(baseSpeed)
    motor_rechts.run(baseSpeed)

    print(motor_rechts)
#Linie 12
#Hintergrund 49
#Start 19
    spd=baseSpeed
    while 1:
        color=cs.reflection()
        error = abs(color - targetColor)
        stear = pidStear(color)
  
        if color < targetColor - 4 or color > targetColor + 4:
            motor_rechts.run(stear)
            motor_links.run(0)
        else:
            motor_rechts.run(spd+stear)
            motor_links.run(spd)
        
        print("stear {} speed {} color {} target {} ".format(stear, spd, color, targetColor))
        
#lineFollower()



def seeker():
    roboter=Roboter(speed=baseSpeed)
    us = PortHelper.getSensor(UltrasonicSensor)
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
                roboter.speed = roboter.speed + 5
            if Button.DOWN in btns:
                roboter.speed = roboter.speed - 5
            if Button.RIGHT in btns:
                roboter.steuer = roboter.steuer + 1
            if Button.LEFT in btns:
                roboter.steuer = roboter.steuer - 1
            
            brick.display.clear()
            brick.display.text("Speed {}".format(roboter.speed), (20,60))
            brick.display.text("Steuer {}".format(roboter.steuer))
            wait(10)
            btns = brick.buttons()

        
            
        wait(10)


auswahl=[ (lineFollower, "linie Motor"), (r.linieFolgen, "linie roboter"), (seeker, "rum fahren"), (calibieren, "Kalibieren")]

#lineFollower()

i=0
while 1:
    if i < 0:
        i = len(auswahl) -1 
    if not i < len(auswahl):
        i=0
    debug(i)
    code, name = auswahl[i]
    Reden.reden(name)
    btn = []
    while not any(btn):
        btn = brick.buttons()
        if Button.CENTER in btn:
            Reden.reden(name)
            code()
        if Button.LEFT in btn:
            i+=1
            break
        if Button.RIGHT in btn:
            i-=1
            break
        wait(50)