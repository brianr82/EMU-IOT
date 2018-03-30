import IoTDevice

class IoTVirtualGateway:
    def __init__(self, gateway_name, gateway_app_port,max_number_iot_devices_supported,IoTGatwayHostClient):
        self.gateway_name = gateway_name
        self.gateway_app_port = gateway_app_port
        self.max_number_iot_devices_supported = max_number_iot_devices_supported
        self.current_iot_devices_connected = 0
        self.IoTGatewayHostClient = IoTGatwayHostClient
        self.connectedIoTDevices = []

    def createIoTVirtualGateway(self):
        self.IoTGatewayHostClient.containers.run("brianr82/multinodered:latest", \
                                       detach=True, \
                                       ports={'1880/tcp': self.gateway_app_port}, \
                                       environment={'FLOWS': 'sensor_flows.json'}, \
                                       name='receiver_' + str(self.gateway_app_port) \
                                       )
        new_container = self.IoTGatewayHostClient.containers.get('receiver_' + str(self.gateway_app_port))
        print 'Created Container\t' + new_container.name

    def add_iot_device(self,IoTDeviceToBeAdded):
        #Step 1. Check if IotDevice is correct type
        assert isinstance(IoTDeviceToBeAdded,IoTDevice)
        #Step 2. Check if there is room on this gateway to add one
        if self.checkIfRoomtoAddDevice() == True:
            self.connectedIoTDevices.append(IoTDeviceToBeAdded)
            self.current_iot_devices_connected = self.current_iot_devices_connected + 1


    def remove_iot_device(self):
        if self.current_iot_devices_connected > 0:
            self.current_iot_devices_connected = self.current_iot_devices_connected - 1
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


