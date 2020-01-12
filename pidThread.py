from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from portHelper import PortHelper
from simple_pid.PID import PID
from debug import debug, debugLevel
from threading import Thread
from oszilationDetector import OszilationDetector
from dataDumper import DataDumper

class PidThread(Thread):

    def __init__(self,robot,input,baseSpeed:int=60, oszilationDetector:OszilationDetector=None):
        self.input = input
        self.robot=robot
        self.baseSpeed=baseSpeed
        self.oszilationDetector = oszilationDetector
        self.speed=round(baseSpeed/2)
        self.stear = 0
        self.targetInput=input()
        debug("Target input ",self.targetInput)
        self.pidStear = PID(Kp=-2.5,Ki=-0.,Kd=0.1, setpoint=self.targetInput, output_limits=(-160,160))
        self.pidStear.tunings=(-2.42, -0.43, 0.07)
        robot.drive(0,40,1000)
        self.linksInput=input()
        self.linksTresh = abs(self.targetInput - self.linksInput) / 3
        debug("links input {} tresh {} ".format(self.linksInput,self.linksTresh))
        robot.drive(0,-40,2000)
        self.rechtsInput=input()
        self.rechtsTresh =  abs(self.targetInput - self.rechtsInput) / 3
        debug("rechts input {} tresh {} ".format(self.rechtsInput,self.rechtsTresh))
        robot.drive(0,40,1000)
        


    def run(self):
        spd=self.speed
        lastStear = 0
        debug("PidThread starting main loop")
        if self.oszilationDetector:
            od=self.oszilationDetector
            dd=DataDumper()
            print("pid thread: oszilation detection active")
        while 1:
            input=self.input()
            self.stear = round(self.pidStear(input))
            if self.oszilationDetector:
                self.oszilationDetector.add(input)
                if self.oszilationDetector.oszilating:
                   # self.robot.drive(0,-30,300)
                    tunings = self.pidStear.tunings
                    self.pidStear.tunings = ( tunings[0] + 0.01, tunings[1]+ 0.01, tunings[2] - 0.01)
                    debug("pid thread: new tunings {}".format(tunings))
               # dd.add(meanA=od.meanA, meanB=od.meanB, meanDiff=od.meanDiff, meanQuoat=od.meanQuoat, tuning=tunings[0], stear=self.stear, input=input)    

            if (abs(input - self.linksInput) < self.linksTresh or abs(input - self.rechtsInput) < self.rechtsTresh) and abs(self.stear) > 10:
                if spd > self.baseSpeed/2:
                    self.robot.stop(Stop.BRAKE)
                    if debugLevel > 3:
                        brick.sound.beep()
                    #print("**** Drive back: {} {} {}".format(-1*spd,-lastStear,self.pidStear.dt*1000))
                    #self.robot.driveBase.drive_time(-1*spd,lastStear,self.pidStear.dt*1000)
                spd=self.baseSpeed*0.1
            else:
                spd+=1
                if spd > self.baseSpeed:
                    spd = self.baseSpeed
            self.speed=spd
            lastStear = self.stear
            debug(level=5, showOnBrick=False,msg="Linefollow thread: stear {} speed {} input {} target {} error {} {}".format(self.stear, spd, input, self.targetInput,abs(input - self.linksInput),abs(input - self.rechtsInput)))
            
        debug("PidThread ended main loop")