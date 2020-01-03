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
                achsen_abstand: int=130,
                motor_rechts:Motor = None,
                motor_links:Motor = None,
                speed:int=50,
                speedThread=None): # SpeedThread cannot be imported due to cyclic imports
        
        self.speed = speed
        self.steuer = 0
        self.gyro=PortHelper.getSensor(GyroSensor)
        self._us = None
        self._cs = None
        self.motor_rechts = motor_rechts 
        self.motor_links = motor_links
        self.speedThread=speedThread
        motors = PortHelper.getMotors()
        if not (self.motor_rechts and self.motor_links) and self.gyro:
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

        if not (self.motor_rechts and self.motor_links):
            debug("Motoren raten")
            self.motor_rechts = motors[0]
            self.motor_links  = motors[1]

        self.driveBase = DriveBase(self.motor_links, self.motor_rechts, rad_durchmesser, achsen_abstand)
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
        self.drive(0,30,500)
        linksColor=self.cs.reflection()
        linksTresh = abs(targetColor - linksColor) / 3
        debug("linksColor {} tresh {} ".format(linksColor,linksTresh))
        self.drive(0,-60,500)
        rechtsColor=self.cs.reflection()
        rechtsTresh =  abs(targetColor - rechtsColor) / 3
        debug("rechtsColor {} tresh {} ".format(rechtsColor,rechtsTresh))
        self.drive(0,30,500)
        pidStear = PID(Kp=2,Ki=-0.,Kd=0.1, setpoint=targetColor, output_limits=(-120,120))

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
            debug("stear {} speed {} color {} target {} error {} {}".format(stear, spd, color, targetColor,abs(color - linksColor),abs(color - rechtsColor)), level=2)
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

            if self.us and self.us.distance() < 50:
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
