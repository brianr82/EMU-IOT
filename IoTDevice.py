from IoTNode import *
#from IoTVirtualGateway import *
from abc import ABCMeta, abstractmethod

class IoTDevice(object):
    __metaclass__ = ABCMeta
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding, BoundIoTVirtualGateway):
        assert isinstance(IoTProducerBinding,IoTNode)
        self.IoTDeviceName = IoTDeviceName
        self.IoTDeviceID = IoTDeviceID
        self.IoTProducerBinding = IoTProducerBinding
        self.BoundIoTVirtualGateway = BoundIoTVirtualGateway

    @abstractmethod
    def createVirtualIoTSensor(self):
        pass


    @abstractmethod
    def removeVirtualIoTSensor(self):
        pass