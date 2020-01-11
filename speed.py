from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread#, Event
from portHelper import PortHelper
from debug import debug



class SpeedThread(Thread):

    def __init__(self, min_speed:float=2., sample_size:int=10, checkIntervall:int=100, roboter=None):
        self.gyro = PortHelper.getSensor(GyroSensor)
        self._minSpeed = min_speed
        debug("min speed {}".format(min_speed))
        self._speeds = [min_speed*10] * sample_size
        self._stalled=0
        self._roboter = roboter
        self._intervall = checkIntervall
        self._stopWatch = StopWatch()
        self._lastSpeedCheck = -100
        self._isStalled = False

    def run(self):
    #    f = open("{}.csv".format(self._roboter.speed),"a+")
      
        while self.gyro:
            self._isStalled = self.isStalled()
           # debug(self.getInformation(),level=2)
      #      print("{} {} {}".format(self.gyro.speed(), self.__mittelwert(self._speeds),self._stalled))
            wait( self._intervall )

    @property
    def roboter(self):
        return self._roboter

    @roboter.setter
    def roboter(self, roboter):
        self._roboter = roboter

    def __addElement(self, lst, val):
        lst[1:] = lst[:-1]
        lst[0] = abs(val)

    def __mittelwert(self, lst):
        mittel = sum(lst) / len(lst)
        return mittel

    @property
    def minSpeed(self):
        try:
            return abs( self._roboter.speed / 50 )
        except:
            pass
        return self._minSpeed

    def __call__(self):
        return self._isStalled

    def hasSpeed(self):
        if self.gyro is None:
            return True
        if self._stopWatch.time() - self._lastSpeedCheck > self._intervall/2:
            self.__addElement(self._speeds, abs(self.gyro.speed()))
            self._lastSpeedCheck = self._stopWatch.time()
        speed = self.__mittelwert(self._speeds)
        return speed >= self.minSpeed

    def isStalled(self):
        if self.gyro is None:
            return False
        if not self.hasSpeed():
            debug(self.getInformation())
            self._stalled += 1
        else:
            self._stalled -= 1
        if self._stalled < 0:
            self._stalled = 0
        return self._stalled > 10

    def getInformation(self):
        return "Stalled {} -> Mittel: {} Schwelle: {} liste {}".format(self._stalled, self.__mittelwert(self._speeds), self._minSpeed, self._speeds)

        
