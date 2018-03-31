from IoTNode import *
from IoTDevice import *


class IoTProducerHost(IoTNode):
    def __init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode):
        IoTNode.__init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode)
        self.virtualIoTDeviceList = []

    def addVirtualIoTDevice(self,new_iot_device_to_add):
        assert isinstance(new_iot_device_to_add,IoTDevice)
        self.virtualIoTDeviceList.append(new_iot_device_to_add)
        print new_iot_device_to_add.IoTDeviceName + ' added'


    def removeVirtualIoTDevice(self,existing_iot_device_to_delete):
        assert isinstance (existing_iot_device_to_delete, IoTDevice)
        self.virtualIoTDeviceList.remove(existing_iot_device_to_delete)
        print existing_iot_device_to_delete.IoTDeviceName + ' removed'
