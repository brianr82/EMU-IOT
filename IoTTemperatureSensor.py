from IotTDevice import *

class IotTemperatureSensor(IotTDevice):
    def __init__(self, targetIoTGateway, TemperatureSensorName):

        assert isinstance(targetIoTNode, IoTNode)
        self.targetIoTNode = targetIoTNode
        self.sensorID = TemperatureSensorName
