from pybricks.tools import print, wait, StopWatch
debugLevel=2

def debug(msg, level=1):
    if not level > debugLevel:
        print("DBG({}/{}: >{}<)".format(level,debugLevel,msg))