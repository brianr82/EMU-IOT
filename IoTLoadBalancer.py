from IoTNetwork import *
import IoTNode
from IoTGatewayHost import IoTGatewayHost
from IoTProducerHost import IoTProducerHost
from IoTDockerController import stopAndRemoveContainers
from IoTDockerController import getContainerCount
import random


class IoTLoadBalancer:
    def __init__(self, balancer_name,parent_iot_network):

        assert isinstance(parent_iot_network, IoTNetwork)
        self.parent_IoTNetwork = parent_iot_network
        self.balancer_name = balancer_name
        self.distribution_policy = 'fill_first'



    def get_current_iot_device_count(self):
        total_count = 0

        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTProducerHost):
                container_list = node.NodeDockerRemoteClient.containers.list(all)
                total_count += len(container_list)
                #print 'TEST:',total_count

        return total_count


    def get_current_iot_gateway_count(self):
        total_count = 0

        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTGatewayHost):
                container_list = node.NodeDockerRemoteClient.containers.list(all)
                total_count += len(container_list)

        return total_count

    def getIoTHostGatewayList(self):
        virtual_iot_gateway_node_list = []
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTGatewayHost):
                virtual_iot_gateway_node_list.append(node)
        return virtual_iot_gateway_node_list


    def remove_all_iot_devices(self):
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance(node, IoTProducerHost):
                #if i.NodeType == 'IoT_Device_Host':
                stopAndRemoveContainers(node.NodeDockerRemoteClient)


    def remove_all_gateways(self):
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTGatewayHost):
                stopAndRemoveContainers(node.NodeDockerRemoteClient)


    def set_distribution_policy_balanced(self):
        self.distribution_policy = 'fill_first'


    def set_distribution_policy_random(self):
        self.set_distribution_policy_random = 'random'



    def get_target_iot_device_edge(self, action):


        if self.distribution_policy == 'random':
            producer_host_node_list = []
            # if the action is to create we need to find IoT producer node that can take it
            if action == 'create':
                for node in self.parent_IoTNetwork.IoTNodeList:
                    # check to see if the node is less than the max the edge can handle
                    if isinstance(node, IoTProducerHost) and getContainerCount(node.NodeDockerRemoteClient) < IoTProducerHost.max_allowed_iot_devices_on_this_host:
                        producer_host_node_list.append(node)

                # choose one at random
                selected_random_node = random.choice(producer_host_node_list)
                selected_edge = selected_random_node
                return selected_edge
            # if the action is to destroy at random we need to find any IoT sensor
            if action == 'destroy':
                for node in self.parent_IoTNetwork.IoTNodeList:
                    # check to see if the node has at least one sensor on it, if it does add it to the list of choices
                    if isinstance(node, IoTProducerHost) and getContainerCount(node.NodeDockerRemoteClient) > 0:
                        producer_host_node_list.append(node)
                # choose one IoT node at random
                selected_random_node = random.choice(producer_host_node_list)
                selected_edge = selected_random_node
                return selected_edge


        # policy for filling each producer host in order of instantiation
        if self.distribution_policy == 'fill_first':
            if action == 'create':
                for found_node in self.parent_IoTNetwork.IoTNodeList:
                    # check to see if the node is less than the max the edge can handle
                    if isinstance(found_node, IoTProducerHost) and getContainerCount(found_node.NodeDockerRemoteClient) < found_node.max_allowed_iot_devices_on_this_host:
                        return found_node







    def iot_network_cleanup(self):
        print ('IoT_Device Count  is ', self.get_current_iot_device_count())
        print ('IoT_Gateway Count  is ', self.get_current_iot_gateway_count())
        if self.get_current_iot_device_count() > 0 or self.get_current_iot_gateway_count() > 0:
            print ('Found some lingering iot devices and gateways on the network.....')
            print ('Now removing old virtual iot devices and gateways.....')
            self.remove_all_iot_devices()
            self.remove_all_gateways()
            print ('After cleaning the iot device count is now ', self.get_current_iot_device_count())
            print ('After cleaning the iot gateway count is now ', self.get_current_iot_device_count())
            print ('Environment is clean and ready to go.....')
        else:
            print ('Environment is clean and ready to go.....')
