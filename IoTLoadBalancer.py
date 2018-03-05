from IoTNetwork import *
from dockerSensor import stopAndRemoveContainers
from dockerSensor import getContainerCount
import random


class IoTLoadBalancer:
    def __init__(self, balancer_name,parent_iot_network):

        assert isinstance(parent_iot_network, IoTNetwork)
        self.parent_IoTNetwork = parent_iot_network
        self.balencer_name = balancer_name
        self.distribution_policy = 'random'
        self.max_iot_devices_per_edge = 500


    def get_current_iot_device_count(self):
        total_count = 0

        for i in self.parent_IoTNetwork.IoTNodeList:
            if i.NodeType == 'IoT_Device':
                container_list = i.NodeDockerRemoteClient.containers.list(all)
                total_count = len(container_list)

        return total_count


    def remove_all_iot_devices(self):
        for i in self.parent_IoTNetwork.IoTNodeList:

            if i.NodeType == 'IoT_Device':
                stopAndRemoveContainers(i.NodeDockerRemoteClient)


    def remove_all_gateways(self):
        for i in self.parent_IoTNetwork.IoTNodeList:
            if i.NodeType == 'Gateway':
                stopAndRemoveContainers(i.NodeDockerRemoteClient)


    def set_distribution_policy_balanced(self):
        self.distribution_policy = 'balanced'


    def set_distribution_policy_random(self):
        self.set_distribution_policy_random = 'random'


    def get_target_iot_device_edge(self, action):

        if self.distribution_policy == 'random':
            iot_device_node_list = []
            # if the action is to create we need to find IoT sensor nodes that can take it
            if action == 'create':
                for node in self.parent_IoTNetwork.IoTNodeList:
                    # check to see if the node is less than the max the edge can handle
                    if node.NodeType == 'IoT_Device' and getContainerCount(
                            node.NodeDockerRemoteClient) < self.max_iot_devices_per_edge:
                        iot_device_node_list.append(node)

                # choose one at random
                selected_random_node = random.choice(iot_device_node_list)
                selected_edge = selected_random_node

            # if the action is to destroy at random we need to find any IoT sensor
            if action == 'destroy':
                for node in self.parent_IoTNetwork.IoTNodeList:
                    # check to see if the node has at least one sensor on it, if it does add it to the list of choices
                    if node.NodeType == 'IoT_Device' and getContainerCount(node.NodeDockerRemoteClient) > 0:
                        iot_device_node_list.append(node)
                # choose one IoT node at random
                selected_random_node = random.choice(iot_device_node_list)
                selected_edge = selected_random_node

        # to be implemented
        # if self.distribution_policy == 'balanced':


        return selected_edge