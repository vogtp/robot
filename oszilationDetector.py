from arrayFixed import ArrayFixed
from pybricks.tools import StopWatch, wait
from pybricks import ev3brick as brick
from debug import debug, debugLevel
from threading import Thread
import _thread

class OszilationDetector(Thread):
    def __init__(self, maxElements:int=10, defaultValue=None):
        self.values = ArrayFixed(60)
        self.windowA = ArrayFixed(30)
        self.windowB = ArrayFixed(30)
        self.meanDiff = 0
        self.meanQuoat= 0
        self.meanA = 0
        self.meanB = 0
        self.oszilating=False
        self.sw = StopWatch()
        self.running=False
        self.rlock = _thread.allocate_lock()

    

    def run(self):
        debug("OszilationDetector thread started")
        self.running=True
        oldInput=0
        while self.running:
            try:
                if hasattr(self, "input"):
                    self.rlock.acquire()
                    input = self.input
                    self.rlock.release()
                    if input != oldInput:
                        self._add(input)
                        oldInput=input
            except:
                debug("Oszilationdetection: Cannot set input")
                wait(100)
            wait(2)
        self.running=False

            

        debug("OszilationDetector thread ended")

    def add(self,value):
        if self.running:
            self.rlock.acquire()
            self.input=value
            self.rlock.release()
        else:
            self._add(value)


    def _add(self,value):
        time=self.sw.time()
        self.values.add((time, value))
        self.windowB.add((time, abs(value)))
        self.windowA.add(self.windowB[0])
        self.meanA=self.windowA.mean(lambda a: a[1])
        self.meanB=self.windowB.mean(lambda a: a[1])
        self.meanDiff=self.meanA-self.meanB
        if self.meanB != 0:
            self.meanQuoat=abs(self.meanA/self.meanB)
        if abs(self.meanDiff) > 20:
            self.oszilating=True
            debug("Oszilation: mean diff {}".format(self.meanDiff))
            if debugLevel > 1:
                brick.sound.beep()
        if abs(self.meanDiff) < 10:
            self.oszilating=False 

    def __str__(self):
        return "diff {:0>2} A {:0>2} b {:0>2}".format(self.meanDiff,self.meanA,self.meanB)

