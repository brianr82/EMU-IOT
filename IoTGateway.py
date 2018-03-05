from IoTNode import *

class IoTGateway(IoTNode):
    def __init__(self, gateway_name, gateway_app_port,max_number_iot_devices_supported):
        assert isinstance(gateway_name, IoTGateway)
        self.gateway_name = gateway_name
        self.gateway_app_port = gateway_app_port
        self.max_number_iot_devices_supported = max_number_iot_devices_supported
