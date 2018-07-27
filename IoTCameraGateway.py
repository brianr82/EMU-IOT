from IoTVirtualGateway import *
from IoTCamera import *
from IoTDeviceType import *

class IoTCameraGateway(IoTVirtualGateway):
    def __init__(self, gateway_name, gateway_app_port, max_number_iot_devices_supported, IoTGatewayHost, DeviceType):
        IoTVirtualGateway.__init__ (self, gateway_name, gateway_app_port, max_number_iot_devices_supported, IoTGatewayHost,DeviceType)

        assert(self.DeviceType == IoTDeviceType.camera)\
            ,'Your supplied:' + self.DeviceType.value + ', expected: ' + IoTDeviceType.camera.value

        self.docker_container_name = self.gateway_name + '_' + self.DeviceType.value

    def createIoTVirtualGateway(self):
        self.IoTGatewayHostClient.containers.run("brianr82/multinodered:latest", \
                                       detach=True, \
                                       ports={'1880/tcp': self.gateway_app_port}, \
                                       environment={'FLOWS': 'sensor_flows.json'}, \
                                       name=self.docker_container_name \
                                       )
        new_container = self.IoTGatewayHostClient.containers.get(self.docker_container_name)
        print ('Created Container\t' + new_container.name)

    def add_iot_device(self,IoTDeviceToBeAdded):
        #Step 1. Check if IotDevice is correct type
        assert isinstance(IoTDeviceToBeAdded,IoTCamera)
        #Step 2. Check if there is room on this gateway to add one
        if self.checkIfRoomtoAddDevice() == True:
            self.connectedIoTDevices.append(IoTDeviceToBeAdded)
            self.current_iot_devices_connected = self.current_iot_devices_connected + 1
        print ('Number of devices allowed connect to this virtual gateway: ' + str(self.max_number_iot_devices_supported))
        print ('Number of devices now connected to this virtual gateway: ' + str(self.current_iot_devices_connected))