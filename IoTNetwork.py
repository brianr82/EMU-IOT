
from IoTNode import *


class IoTNetwork:
    def __init__(self, NetworkName):
        self.NetworkName = NetworkName
        self.IoTNodeList = []

    def add_new_IoTNode(self, node_to_add):
        assert isinstance(node_to_add, IoTNode)
        self.IoTNodeList.append(node_to_add)

