from debug import debug
from pybricks.tools import  StopWatch, wait
from threading import Thread
import _thread

class DataDumper(Thread):

    FILENAME="zDatadumper_{}.csv"
    HEADER_TIME="time"

    def __init__(self):
        self.sw = StopWatch()
        self.dataSets = {}
        self.openFiles = {}
        self.running = False
        self.rlock = _thread.allocate_lock()
        super().__init__()

    

    def run(self):
        self.running = True
        self.input = []
        self.dataset = []
        debug("Started datadumper thread",0)
        while self.running:
            if len(self.input) > 0:
                self.rlock.acquire()
                ds = self.dataset.pop(0)
                args = self.input.pop(0)
                self.rlock.release()
                self._add(ds,args)
            else:
                wait(10)
        debug("Stopped datadumper thread")
            


    def add(self, dataset:str, **kwargs): 
        if self.running:
            # add for the thread
            self.rlock.acquire()
            self.dataset.append(dataset)
            self.input.append(kwargs)
            self.rlock.release()
        else:
            self._add(dataset, kwargs)

    def _add(self, dataset:str, kwargs:dict): 
        if "time" not in kwargs:
            kwargs["time"] = self.sw.time()
        if not dataset in self.dataSets.keys():
            self._initFile(dataset, kwargs)
        values=[]
        for key in self.dataSets[dataset]:
            val="{}".format(kwargs[key])
            if "," in val:
                if "'" in val:
                    val=val.replace("'","\\'")
                val="'{}'".format(val)
                
            values.append(val)
        #self._write(dataset,",".join(values))
        self._write(dataset,values)
        

    def _initFile(self, dataset, args:dict): 
        self.openFiles[dataset]=open(self.FILENAME.format(dataset), 'w')
        headers=[self.HEADER_TIME]
        for name in args.keys():
            if not name is self.HEADER_TIME:
                headers.append(name)
        self.dataSets[dataset]=headers
     #   self._write(dataset, ",".join(headers))
        self._write(dataset, headers)
        debug("Datadumper: dataset {} headers {}".format(dataset,",".join(headers)))

    def _write(self,dataset, output):
        print(*output,sep=",",file=self.openFiles[dataset])
        # self.openFiles[dataset].write(output+"\n")

if __name__ == '__main__':
        # time does not work due to the pybrick wrapper
        dd = DataDumper()
        dd.add("TestData", x=1, y="direct",z=[1,2,3,4])
        dd.start()
        wait(100)
        dd.add("TestData", x=10, y="thread",z=[11,12,13,14])
        wait(100)
        dd.add("TestData", x=20, y="thread",z=[21,22,23,'24'])
        wait(100)
        dd.running=False
