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

baseSpeed=50


def lineFollower():
    cs = PortHelper.getSensor(ColorSensor)
    print("ambient {} color {} reflection {} rgb {}".format(cs.ambient(),cs.color(),cs.reflection(),cs.rgb()))
    motor_links=Motor(Port.D)
    motor_rechts=Motor(Port.B)
    #papiHilfe.wartenAmAnfang()
    targetColor=cs.reflection()

    #pid = PID(10,5,2., targetColor, output_limits=(-190,190))
    pidStear = PID(Kp=-2,Ki=-.0,Kd=-.0, setpoint=targetColor, output_limits=(-60,60))
    pidSpeed = PID(3,1,3, 20, output_limits=(20,100))

    motor_rechts.dc(50)
    motor_links.dc(50)
    motor_links.run(baseSpeed)
    motor_rechts.run(baseSpeed)

    print(motor_rechts)

    spd=50
    while 1:
        color=cs.reflection()
        error = abs(color - targetColor)
        stear = pidStear(color)
        #spd = round(pidSpeed(color))
        if error > 10:
            spd-=error
            if spd < 0:
                if abs(stear) < 5:
                    spd = 5
                else:
                    spd = 0
        if error > 5:
            spd-=1
            if spd < 0:
                spd = 15
        else:
            spd+=1
        if spd > 50:
            spd=50
        print("stear {} speed {} color {} target {} error {}".format(stear, spd, color, targetColor,error))
        motor_rechts.dc(spd+stear)
        motor_links.dc(spd-stear)

def lineFollowerRobot():
    cs = PortHelper.getSensor(ColorSensor)
    print("ambient {} color {} reflection {} rgb {}".format(cs.ambient(),cs.color(),cs.reflection(),cs.rgb()))
    roboter=Roboter(speed=baseSpeed, motor_links=Motor(Port.D), motor_rechts=Motor(Port.B))
    #papiHilfe.wartenAmAnfang()
    targetColor=cs.reflection()

    #pid = PID(10,5,2., targetColor, output_limits=(-190,190))
    pidStear = PID(Kp=4,Ki=-0.1,Kd=-0.1, setpoint=targetColor, output_limits=(-120,120))
    pidSpeed = PID(3,1,3, 20, output_limits=(20,100))

    spd=50
    while 1:
        color=cs.reflection()
        error = abs(color - targetColor)
        stear = round(pidStear(color))
        #spd = round(pidSpeed(color))
        if error > 10:
            spd-=error
            if spd < 20:
                spd = 20
        elif error < 2:
            spd+=5
        print("stear {} speed {} color {} target {} error {}".format(stear, spd, color, targetColor,error))
        roboter.drive(stearing=stear, speed=spd)
    
def seeker():
    roboter=Roboter(speed=baseSpeed)
    us = PortHelper.getSensor(UltrasonicSensor)
    speed = Speed(roboter=roboter)
    speed.start()
    while 1:
        drive()
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


lineFollower()