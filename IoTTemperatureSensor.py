from IoTNode import *

class IotTemperatureSensor(IoTNode):
    def __init__(self, targetIoTNode, TemperatureSensorName):

        assert isinstance(targetIoTNode, IoTNode)
        self.targetIoTNode = targetIoTNode
        self.sensorID = TemperatureSensorName
