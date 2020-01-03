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
                radDurchmesser: int=56, 
                achsenAbstand: int=130,
                motorRechts:Motor = None,
                motorLinks:Motor = None,
                speed:int=80,
                speedThread=None): # SpeedThread cannot be imported due to cyclic imports
        
        self.speed = speed
        self.steuer = 0
        self.gyro=PortHelper.getSensor(GyroSensor)
        if self.gyro:
            self.gyro.reset_angle(0)
        self._us = None
        self._cs = None
        self.motorRechts = motorRechts 
        self.motorLinks = motorLinks
        self.speedThread=speedThread
        if speedThread:
            speedThread.roboter = self
        motors = PortHelper.getMotors()
        if not (self.motorRechts and self.motorLinks) and self.gyro:
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
                    self.motorRechts = m
                elif angle < 0:
                    print("Linker Motor","{}".format(m).split("\n")[2].replace("\t",""))
                    debug(m,level=5)
                    self.motorLinks = m 
                m.run_angle(-1*checkSpeed,checkDegs)

        if not (self.motorRechts and self.motorLinks):
            debug("Motoren raten")
            self.motorRechts = motors[0]
            self.motorLinks  = motors[1]

        self.driveBase = DriveBase(self.motorLinks, self.motorRechts, radDurchmesser, achsenAbstand)
        #self.kraft = 30

    @property
    def cs(self):
        if not self._cs:
            self._cs = PortHelper.getSensor(ColorSensor)
            if self._cs:
                print("New ColorSensor: ambient {} color {} reflection {} rgb {}".format(self._cs.ambient(),self._cs.color(),self._cs.reflection(),self._cs.rgb()))
        if not self._cs:
            print("No ColorSensor found")
        return self._cs

    @property
    def us(self):
        if not self._us:
            self._us = PortHelper.getSensor(UltrasonicSensor)
            if self._us:
                print("New UltrasonicSensor: distance {} presence {}".format(self._us.distance(),self._us.presence()))
        if not self._us:
            print("No UltrasonicSensor found")
        return self._us

    def zeigGyro(self):
        if self.gyro:
            print("Gyro: Speed {} Angle {}".format(self.gyro.speed(),self.gyro.angle()))
        else:
            print("No Gyrosensor")

    @property
    def kraft(self):
        return self._kraft

    @kraft.setter
    def kraft(self, kraft:int):
        self._kraft = kraft
        self.motorLinks.dc(kraft)
        self.motorRechts.dc(kraft)

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

    def drehen(self,winkel:int,fehler:int=0):
        self.gyro.reset_angle(0)
        self.drehenAufWinkel(winkel)

    def drehenAufWinkel(self, winkel:int, fehler:int=0):
        winkel=-1*winkel
        winkelPid=PID(-5,0,0,winkel, output_limits=(-50,50))
        angle = self.gyro.angle()
        while  abs(winkel - angle) > fehler:
            stear = winkelPid(angle)
            if stear < 5:
                stear*=3
            self.drive(0,stear)
            debug("drehenAufWinkel: ziel {} angle {} stear {}".format(winkel, angle,stear),level=2)
            angle = self.gyro.angle()
            #wait(10)
        debug("drehenAufWinkel: ziel {} ist {}".format(winkel, angle ))    
        self.stop(Stop.BRAKE)

    def ausweichen(self):
        # if self.us and self.us.distance() < 2550:
        #     self.__ausweichen_pid()
        # else:
            self.__ausweichenSimpel()

    def __ausweichenPid(self):
        pid=PID(1,0,0,2551,None)
        sw = StopWatch()
        while 1 or sw.time() < 13000:
            a = pid(self.us.distance())
            debug("PID ausweichen: Steuer {} dist {}".format(a,self.us.distance()))
            self.drive(0,a)
            wait(100)

    def __ausweichenSimpel(self):
        if not self.speed == 0:
            speed=self.speed*-1
            time=abs(100/speed)
            time*=1000
            print("Ausweichen: speed {} time {}".format(speed,time))
            self.drive(speed,0,time)
            self.drive(0,30,3000)

    def stop(self,action:Stop=Stop.COAST):
        self.driveBase.stop(action)

    def linieFolgen(self):
        debug("linieFolgen")
        baseSpeed=self.speed # optimal: 80
        targetColor=self.cs.reflection()
        debug("Target color ",targetColor)
        self.drive(0,40,1000)
        linksColor=self.cs.reflection()
        linksTresh = abs(targetColor - linksColor) / 3
        debug("linksColor {} tresh {} ".format(linksColor,linksTresh))
        self.drive(0,-40,2000)
        rechtsColor=self.cs.reflection()
        rechtsTresh =  abs(targetColor - rechtsColor) / 3
        debug("rechtsColor {} tresh {} ".format(rechtsColor,rechtsTresh))
        self.drive(0,40,1000)
        pidStear = PID(Kp=-2.5,Ki=-0.,Kd=0.1, setpoint=targetColor, output_limits=(-160,160))

        spd=baseSpeed
        lastStear = 0
        while 1:
            color=self.cs.reflection()
            stear = round(pidStear(color))
            if (abs(color - linksColor) < linksTresh or abs(color - rechtsColor) < rechtsTresh) and abs(stear) > 10:
                if spd > 10:
                    self.stop(Stop.BRAKE)
                    brick.sound.beep()
                    print("**** Drive back: {} {} {}".format(-1*spd,lastStear,pidStear.dt*1000))
                    self.drive(-1*spd,lastStear,pidStear.dt*1000)
                spd=0
            else:
                spd+=1
                if spd > baseSpeed:
                    spd = baseSpeed
            debug(level=2, msg="stear {} speed {} color {} target {} error {} {}".format(stear, spd, color, targetColor,abs(color - linksColor),abs(color - rechtsColor)))
            self.drive(stearing=stear, speed=spd)
            lastStear = stear

    def rumFahren(self):
        baseSpeed=self.speed
        self.speedThread.start()
        while 1:
            self.drive()
            if self.speedThread and self.speedThread():
                brick.sound.beep()
                self.ausweichen()

            if self.us and self.us.distance() < self.speed/4:
                self.stop()
                brick.sound.file(SoundFile.DETECTED)
                self.ausweichen()

            btns = brick.buttons()
            while any(btns):
                self.stop()
                if Button.CENTER in btns:
                    self.steuer = 0
                    self.speed = baseSpeed
                if Button.UP in btns:
                    self.speed = self.speed + 5
                if Button.DOWN in btns:
                    self.speed = self.speed - 5
                if Button.RIGHT in btns:
                    self.steuer = self.steuer + 1
                if Button.LEFT in btns:
                    self.steuer = self.steuer - 1
                
                brick.display.clear()
                brick.display.text("Speed {}".format(self.speed), (20,60))
                brick.display.text("Steuer {}".format(self.steuer))
                wait(10)
                btns = brick.buttons()    
            wait(10)

        self.speedThread.stop()
