from IoTGateway import *

class IotTDevice:
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTGatewayBinding):
        assert isinstance(IoTGatewayBinding, IoTGateway)
        self.IoTDeviceName = IoTDeviceName
        self.IoTDeviceID = IoTDeviceID
        self.IoTGatewayBinding = IoTGatewayBinding

