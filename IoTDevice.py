from IoTNode import *
#from IoTVirtualGateway import *

class IoTDevice:
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding):
        assert isinstance(IoTProducerBinding,IoTNode)
        self.IoTDeviceName = IoTDeviceName
        self.IoTDeviceID = IoTDeviceID
        self.IoTProducerBinding = IoTProducerBinding

