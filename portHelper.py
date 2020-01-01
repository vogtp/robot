from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import inspect 

class PortHelper:

    sensorPorts = [(Port.S1,"Port.S1"), (Port.S2,"Port.S2"), (Port.S3,"Port.S3"), (Port.S4,"Port.S4")]
    motorPorts = [(Port.A,"Port.A"), (Port.B,"Port.B"), (Port.C,"Port.C"), (Port.D,"Port.D")]

    @staticmethod
    def getSensor(sensorType):
        for port, name in PortHelper.sensorPorts:
            try:
                sensor = sensorType(port)
                s = "{}".format(sensor)
                s=s.replace("<","").split(" ")[0]
                print("Found {} on {}".format(s,name))
                return sensor
            except:
                pass

    @staticmethod
    def getMotors():
        motors = []
        for port, name in PortHelper.motorPorts:
            try:
                motor = Motor(port)
                s = "{}".format(motor)
                s=s.replace("<","").split(" ")[0]
                print("Found {} on {}".format(s,name))
                motors.append(motor)
            except: # Exception as e:
               # print(e)
                pass
        return motors

   
        