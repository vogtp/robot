from pybricks.tools import print, wait, StopWatch
from pybricks import ev3brick as brick
debugLevel=2

def debug(msg, level=1, showOnBrick=True):
    if not level > debugLevel:
        print("DBG({}/{}: >{}<)".format(level,debugLevel,msg))
        if showOnBrick:
            brick.display.text(msg)


            