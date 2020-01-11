from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor
#from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
#from portHelper import PortHelper
from debug import debug, debugLevel
from threading import Thread

class SensorMotorThread(Thread):

    def __init__(self, motor:Motor,angleThreshold=7,motorSpeed=40):
        self.motor = motor
        if not self.motor:
            return
        self.motor.set_dc_settings(40,0)
        self.posAngle=0
        self.negAngle=0
        self.angleThresh=angleThreshold
        self.motorSpeed=motorSpeed
        self.moveMotor=0
        self.moveCenter()

    def run(self):
        if not self.motor:
            return
        self.motorLoop()
        # self.moveCenter2()
        # while 1:
        #     brick.sound.beep()
        #     self.motor.run_target(-1*abs(self.motorSpeed),self.negAngle+self.angleThresh)
        #     self.motor.run_target(abs(self.motorSpeed),self.posAngle-self.angleThresh)

    def moveCenter2(self):
        if not self.motor:
            return
        self.moveMotor=0
        self._motorLoop(lambda : self.posAngle == 0 or self.negAngle == 0)
        if self.motor.angle() < 0:
            self.motor.run_target(abs(self.motorSpeed),0)
        else:
            self.motor.run_target(abs(self.motorSpeed),0)
        debug("Sensor Motor: moved to center")

    def moveCenter(self):
        if not self.motor:
            return
        self.moveMotor=0
        #self._motorLoop(lambda : self.posAngle == 0 or self.negAngle == 0)
        self.motor.run_until_stalled(abs(self.motorSpeed))
        self.posAngle=self.motor.angle()
        self.motor.run_until_stalled(-1*abs(self.motorSpeed))
        self.negAngle=self.motor.angle()
        debug(level=6,msg="Sensor Motor: angle pos {} neg {}".format(self.posAngle,self.negAngle))
        tot =abs(self.posAngle) + abs(self.negAngle)
        self.motor.reset_angle(tot/-2)
        self.motor.run_target(abs(self.motorSpeed),0)

    def motorLoop(self):
        if not self.motor:
            return
        self.moveMotor=1
        self._motorLoop(lambda : self.moveMotor)

    def _motorLoop(self, condition):
        if not self.motor:
            return
        debug("Sensor Motor: loop started")
        while condition():
            curAngle = self.motor.angle()
            if self.posAngle != 0 and self.negAngle != 0 and (
                    ( (curAngle > self.posAngle or curAngle  >  self.posAngle - self.angleThresh )  and self.motorSpeed > 0 ) 
                    or ( (curAngle < self.negAngle or curAngle < self.negAngle + self.angleThresh )  and self.motorSpeed < 0) ):
                debug(level=6,msg="Sensor Motor: trun: speed {} pos check {} neg check {} ".format(self.motorSpeed,abs(curAngle - self.posAngle),abs(curAngle + self.negAngle)))
                self.motorSpeed*=-1
            self.motor.run(self.motorSpeed)
            self.ifStalledUpdateMaxAngles()
            debug(level=5,msg="Sensor Motor: angle {} speed {}".format(self.motor.angle(),self.motor.speed()))
            wait(10)
        debug("Sensor Motor: loop stopped")

    def ifStalledUpdateMaxAngles(self):
        if not self.motor:
            return
        if self.motor.stalled():
            if self.motorSpeed < 0:
                self.negAngle=self.motor.angle()+self.angleThresh
                if self.negAngle == 0:
                    self.posAngle,self.negAngle=0,-50
                    self.motor.reset_angle(self.negAngle)
                debug("Sensor Motor: new neg angle {} (speed {})".format(self.negAngle, self.motorSpeed))
                if self.posAngle == 0 or self.negAngle == 0:
                    self.motorSpeed*=-1
                    self.motor.run(self.motorSpeed)
                else:
                    tot =abs(self.posAngle) + abs(self.negAngle)
                    self.motor.reset_angle(tot/-2)
            elif self.motorSpeed > 0:
                self.posAngle=self.motor.angle()-self.angleThresh
                if self.posAngle == 0:
                    self.posAngle,self.negAngle=50,0
                    self.motor.reset_angle(self.posAngle)
                debug("Sensor Motor: new pos angle {} (speed {})".format(self.posAngle,self.motorSpeed))
                if self.posAngle == 0 or self.negAngle == 0:
                    self.motorSpeed*=-1
                    self.motor.run(self.motorSpeed)
                else:
                    tot =abs(self.posAngle) + abs(self.negAngle)
                    self.motor.reset_angle(tot/2)
