from IoTDevice import *
from abc import ABCMeta, abstractmethod

class IoTVirtualGateway(object):
    __metaclass__ = ABCMeta
    def __init__(self, gateway_name, gateway_app_port,max_number_iot_devices_supported,IoTGatewayHost,DeviceType):
        self.gateway_name = gateway_name
        self.gateway_app_port = gateway_app_port
        self.max_number_iot_devices_supported = max_number_iot_devices_supported
        self.current_iot_devices_connected = 0
        self.IoTGatewayHostClient = IoTGatewayHost.NodeDockerRemoteClient
        self.connectedIoTDevices = []
        self.DeviceType = DeviceType


    @abstractmethod
    def createIoTVirtualGateway(self):
        pass

    @abstractmethod
    def add_iot_device(self,IoTDeviceToBeAdded):
        pass


    def remove_iot_device(self,IoTDeviceToBeRemoved):
        if self.current_iot_devices_connected > 0:
            self.connectedIoTDevices.remove (IoTDeviceToBeRemoved)
            self.current_iot_devices_connected = self.current_iot_devices_connected - 1
            print ('Number of devices allowed connect to this virtual gateway: ' + str (
                self.max_number_iot_devices_supported))
            print ('After Removal number of devices now connected to this virtual gateway: ' + str (
                self.current_iot_devices_connected))
            return True
        else:
            print ('All devices already removed')
            return False


    def checkIfRoomtoAddDevice(self):
        if self.current_iot_devices_connected < self.max_number_iot_devices_supported:
            return True
        else:
            print ('Max Number of devices reached')
            return False
