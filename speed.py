from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from roboter import Roboter
from threading import Thread#, Event
from portHelper import PortHelper
from debug import debug

class SpeedThread(Thread):

    def __init__(self, min_speed:float=.9, sample_size:int=10, checkIntervall:int=100, roboter:Roboter=None):
        self.gyro = PortHelper.getSensor(GyroSensor)
        self._minSpeed = min_speed
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
            debug(self.getInformation(),level=2)
         #   f.write("{},{}\n".format(self.gyro.speed(), self.__mittelwert(self._speeds))
            wait(self._intervall)

    def __addElement(self, lst, val):
        lst[1:] = lst[:-1]
        lst[0] = abs(val)

    def __mittelwert(self, lst):
        mittel = sum(lst) / len(lst)
        return mittel

    @property
    def minSpeed(self):
        # if self._roboter:
        #     min = abs( self._roboter.speed / 25 )
            
        #     debug("Got Min speed = {}".format(min))
        #     self._minSpeed = min
        #     if min < self._minSpeed:
        #         debug("Min speed = {}".format(min))
        #         return min
        return self._minSpeed

    def __call__(self):
        return self._isStalled

    def hasSpeed(self):
        if self.gyro is None:
            return True
        if self._stopWatch.time() - self._lastSpeedCheck > self._intervall/2:
            self.__addElement(self._speeds, self.gyro.speed())
            self._lastSpeedCheck = self._stopWatch.time()
        speed = self.__mittelwert(self._speeds)
        return speed >= self.minSpeed

    def isStalled(self):
        if self.gyro is None:
            return False
        if not self.hasSpeed():
            print(self.getInformation())
            self._stalled += 1
        else:
            self._stalled -= 1
        if self._stalled < 0:
            self._stalled = 0
        return self._stalled > 10

    def getInformation(self):
        return "Stalled {} -> Mittel: {} Schwelle: {} liste {}".format(self._stalled, self.__mittelwert(self._speeds), self._minSpeed, self._speeds)

        
