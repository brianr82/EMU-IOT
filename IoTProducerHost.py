from IoTNode import *
from IoTDevice import *


class IoTProducerHost(IoTNode):
    def __init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode):
        IoTNode.__init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode)
        self.virtualIoTDeviceList = []
        self.max_allowed_iot_devices_on_this_host = 0
        self.IoTDeviceCounter = 0

    def addVirtualIoTDevice(self,new_iot_device_to_add):
        assert isinstance(new_iot_device_to_add,IoTDevice)

        #add device to local list
        self.virtualIoTDeviceList.append(new_iot_device_to_add)
        #add device to IotVirtualGateway
        new_iot_device_to_add.BoundIoTVirtualGateway.add_iot_device(new_iot_device_to_add)

        #increment local counter everytime we add, counter will be used to give each new device a unique id
        self.IoTDeviceCounter  = self.IoTDeviceCounter +1

        print ('Producer Host: ' + new_iot_device_to_add.IoTDeviceName + ' added')
        print ('Producer Host: After adding, the number of devices is: ' + str (self.IoTDeviceCounter))

    def removeVirtualIoTDevice(self,existing_iot_device_to_delete):
        #check if its an IoTDevice
        assert isinstance (existing_iot_device_to_delete, IoTDevice)

        # remove if from list of devices on this host
        self.virtualIoTDeviceList.remove(existing_iot_device_to_delete)

        #remove the device from the virtual gateway
        existing_iot_device_to_delete.BoundIoTVirtualGateway.remove_iot_device (existing_iot_device_to_delete)

        self.IoTDeviceCounter = self.IoTDeviceCounter - 1

        #print the result
        print ('Producer Host: ' + existing_iot_device_to_delete.IoTDeviceName + ' removed')
        print ('Producer Host: After removing, the number of devices is: ' + str(self.IoTDeviceCounter))
