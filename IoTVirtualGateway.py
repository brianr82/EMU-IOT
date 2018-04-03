from IoTDevice import *
from abc import ABCMeta, abstractmethod

class IoTVirtualGateway(object):
    __metaclass__ = ABCMeta
    def __init__(self, gateway_name, gateway_app_port,max_number_iot_devices_supported,IoTGatewayHost):
        self.gateway_name = gateway_name
        self.gateway_app_port = gateway_app_port
        self.max_number_iot_devices_supported = max_number_iot_devices_supported
        self.current_iot_devices_connected = 0
        self.IoTGatewayHostClient = IoTGatewayHost.NodeDockerRemoteClient
        self.connectedIoTDevices = []


    @abstractmethod
    def createIoTVirtualGateway(self):
        pass

    @abstractmethod
    def add_iot_device(self,IoTDeviceToBeAdded):
        pass

    @abstractmethod
    def remove_iot_device(self,IoTDeviceToBeRemoved):
        pass

    @abstractmethod
    def checkIfRoomtoAddDevice(self):
        pass
