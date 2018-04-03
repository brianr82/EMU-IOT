from IoTNode import *
#from IoTVirtualGateway import *
from abc import ABCMeta, abstractmethod

class IoTDevice(object):
    __metaclass__ = ABCMeta
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding):
        assert isinstance(IoTProducerBinding,IoTNode)
        self.IoTDeviceName = IoTDeviceName
        self.IoTDeviceID = IoTDeviceID
        self.IoTProducerBinding = IoTProducerBinding

    @abstractmethod
    def createVirtualIoTSensor(self):
        pass
