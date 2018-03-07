from IoTVirtualGateway import *

class IoTDevice:
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding):
        assert isinstance(IoTVirtualGatewayBinding, IoTVirtualGateway)
        self.IoTDeviceName = IoTDeviceName
        self.IoTDeviceID = IoTDeviceID
        self.IoTVirtualGatewayBinding = IoTVirtualGatewayBinding

