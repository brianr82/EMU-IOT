from IoTNode import *

class IoTGateway(IoTNode):
    def __init__(self, gateway_name):
        assert isinstance(gateway_name, IoTGateway)
        self.gateway_name = gateway_name
        self.starting_port_range = 3000
        self.current_port = 3000
