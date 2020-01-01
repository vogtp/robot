from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from portHelper import PortHelper
from simple_pid.PID import PID
from debug import debug

class Roboter():

    def __init__(self, 
                rad_durchmesser: int=56, 
                achsen_abstand: int=121,
                speed:int=50):
        
        self.speed = speed
        self.steuer = 0
        self.gyro=PortHelper.getSensor(GyroSensor)
        self.us = PortHelper.getSensor(UltrasonicSensor)
        motors = PortHelper.getMotors()
        if self.gyro:
            # gyrosensor um die richitgen motoren zu finden
            checkDegs=30
            checkSpeed=300
            for m in motors:
                self.gyro.reset_angle(0)
                m.run_angle(checkSpeed,checkDegs)
                angle = self.gyro.angle()
                debug("Motorfind: angle {}".format(angle))
                if angle > 0:
                    print("Rechter Motor","{}".format(m).split("\n")[2].replace("\t",""))
                    debug(m,level=5)
                    self.motor_rechts = m
                elif angle < 0:
                    print("Linker Motor","{}".format(m).split("\n")[2].replace("\t",""))
                    debug(m,level=5)
                    self.motor_links = m 
                m.run_angle(-1*checkSpeed,checkDegs)

        if not (self.motor_rechts or self.motor_links):
            debug("Motoren raten")
            self.motor_rechts = motors[0]
            self.motor_links  = motors[1]

        self.driveBase = DriveBase(self.motor_links, self.motor_rechts, rad_durchmesser, achsen_abstand)
        #self.kraft = 30


    @property
    def kraft(self):
        return self._kraft

    @kraft.setter
    def kraft(self, kraft:int):
        self._kraft = kraft
        self.motor_links.dc(kraft)
        self.motor_rechts.dc(kraft)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed:int):
        self._speed = speed
        print("Set speed ",self._speed)

    @property
    def steuer(self):
        return self._stearing

    @steuer.setter
    def steuer(self,stearing:float):
        self._stearing = stearing
        print("Set stearing ",self._stearing)

    def drive(self, speed:float=None, stearing:float=None, time:int=None):
        if speed == None:
            speed = self.speed
        if stearing == None:
            stearing = self.steuer
        if time:
            self.driveBase.drive_time(speed,stearing,time)
        else:
            self.driveBase.drive(speed,stearing)

    def ausweichen(self):
        # if self.us and self.us.distance() < 2550:
        #     self.__ausweichen_pid()
        # else:
            self.__ausweichen_simpel()

    def __ausweichen_pid(self):
        pid=PID(1,0,0,2551,None)
        sw = StopWatch()
        while 1 or sw.time() < 13000:
            a = pid(self.us.distance())
            debug("PID ausweichen: Steuer {} dist {}".format(a,self.us.distance()))
            self.drive(0,a)
            wait(100)

    def __ausweichen_simpel(self):
        if not self.speed == 0:
            speed=self.speed*-1
            time=abs(100/speed)
            time*=1000
            print("Ausweichen: speed {} time {}".format(speed,time))
            self.drive(speed,0,time)
            self.drive(0,30,3000)

    def stop(self,action:Stop=Stop.COAST):
        self.driveBase.stop(action)
