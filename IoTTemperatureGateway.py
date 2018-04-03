from IoTVirtualGateway import *
from IoTTemperatureSensor import *

class IoTTemperatureGateway(IoTVirtualGateway):
    def __init__(self, gateway_name, gateway_app_port, max_number_iot_devices_supported, IoTGatewayHost):
        IoTVirtualGateway.__init__ (self, gateway_name, gateway_app_port, max_number_iot_devices_supported, IoTGatewayHost)

    def createIoTVirtualGateway(self):
        self.IoTGatewayHostClient.containers.run("brianr82/multinodered:latest", \
                                       detach=True, \
                                       ports={'1880/tcp': self.gateway_app_port}, \
                                       environment={'FLOWS': 'sensor_flows.json'}, \
                                       name=self.gateway_name \
                                       )
        new_container = self.IoTGatewayHostClient.containers.get(self.gateway_name)
        print 'Created Container\t' + new_container.name

    def add_iot_device(self,IoTDeviceToBeAdded):
        #Step 1. Check if IotDevice is correct type
        assert isinstance(IoTDeviceToBeAdded,IoTTemperatureSensor)
        #Step 2. Check if there is room on this gateway to add one
        if self.checkIfRoomtoAddDevice() == True:
            self.connectedIoTDevices.append(IoTDeviceToBeAdded)
            self.current_iot_devices_connected = self.current_iot_devices_connected + 1
        print 'Number of devices allowed connect to this virtual gateway: ' + str(self.max_number_iot_devices_supported)
        print 'Number of devices now connected to this virtual gateway: ' + str(self.current_iot_devices_connected)


    def remove_iot_device(self,IoTDeviceToBeRemoved):
        if self.current_iot_devices_connected > 0:
            self.connectedIoTDevices.remove(IoTDeviceToBeRemoved)
            self.current_iot_devices_connected = self.current_iot_devices_connected - 1
            print 'Number of devices allowed connect to this virtual gateway: ' + str (self.max_number_iot_devices_supported)
            print 'After Removal number of devices now connected to this virtual gateway: ' + str (self.current_iot_devices_connected)
            return True
        else:
            print 'All devices already removed'
            return False




    def checkIfRoomtoAddDevice(self):
        if self.current_iot_devices_connected < self.max_number_iot_devices_supported:
            return True
        else:
            print 'Max Number of devices reached'
            return False