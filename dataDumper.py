from debug import debug
from pybricks.tools import  StopWatch

class DataDumper():

    FILENAME="zDatadumper_{}.csv"
    HEADER_TIME="time"

    def __init__(self):
        self.sw = StopWatch()
        self.dataSets = {}
        self.openFiles = {}

    def add(self, dataset:str, **kwargs): 
        if "time" not in kwargs:
            kwargs["time"] = self.sw.time()
        if not dataset in self.dataSets.keys():
            self._initFile(dataset, kwargs)
        values=[]
        for key in self.dataSets[dataset]:
            val="{}".format(kwargs[key])
            if "," in val:
                val="'{}'".format(val)
            print(val)
            values.append(val)
        self._write(dataset,",".join(values))
        

    def _initFile(self, dataset, args:dict): 
        self.openFiles[dataset]=open(self.FILENAME.format(dataset), 'w')
        headers=[self.HEADER_TIME]
        print(args)
        for name in args.keys():
            if not name is self.HEADER_TIME:
                headers.append(name)
        self.dataSets[dataset]=headers
        self._write(dataset, ",".join(headers))
        debug("Datadumper: dataset {} headers {}".format(dataset,",".join(headers)))

    def _write(self,dataset, output):
        self.openFiles[dataset].write(output+"\n")

if __name__ == '__main__':
        dd = DataDumper()
        dd.add("TestData", x=1, y="Bla",z=[1,2,3,4])