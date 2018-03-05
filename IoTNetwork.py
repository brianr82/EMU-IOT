from IoTNode import *


class IoTNetwork:
    def __init__(self, NetworkName):
        self.NetworkName = NetworkName
        self.IoTNodeList = []

    def add_new_IoTNode(self, node_to_add):
        assert isinstance(node_to_add, IoTNode)
        self.IoTNodeList.append(node_to_add)

    def get_current_sensor_count(self):
        total_count = 0

        for i in self.IoTNodeList:
            if i.NodeType == 'Sensor':
                container_list = i.NodeDockerRemoteClient.containers.list(all)
                total_count = len(container_list)

        return total_count
