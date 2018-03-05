
from IoTNode import *


class IoTNetwork:
    def __init__(self, NetworkName):
        self.NetworkName = NetworkName
        self.IoTNodeList = []

    def add_new_IoTNode(self, node_to_add):
        assert isinstance(node_to_add, IoTNode)
        self.IoTNodeList.append(node_to_add)

    def get_IoTNode(self,node_to_find):

        #found_node = [x for x in self.IoTNodeList if x.NodeName == node_to_find]

        for node in self.IoTNodeList:
            if node.NodeName == node_to_find:
                found_node = node
                break

        return found_node

