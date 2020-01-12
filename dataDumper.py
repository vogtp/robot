from debug import debug
import json
import os
from pybricks.tools import print, wait, StopWatch

class DataDumper():

    def __init__(self):
        self.sw = StopWatch()
        self.data = []
        self.dumptofileCount=0

    def getData(self):
        return json.dumps(self.data)

    def add(self, debugLevel:int=10, **kwargs): 
        if "time" not in kwargs:
            kwargs["time"] = self.sw.time()
        self.data.append(kwargs)
        debug( msg="Datadumer: {}".format(kwargs), level=debugLevel)
        self.dumptofileCount += 1
        if self.dumptofileCount > 20:
            self.write()
            self.dumptofileCount=0

    def write(self,fileName:str=None):
        if not fileName:
            fileName='datadumper.json'
        os.rename(fileName, fileName+".old")
        with open(fileName, 'w') as outfile:
            outfile.write(json.dumps(self.data))
        os.unlink(fileName+".old")