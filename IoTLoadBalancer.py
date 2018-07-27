from IoTNetwork import *
from IoTGatewayHost import IoTGatewayHost
from IoTProducerHost import IoTProducerHost


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

    def getIoTHostProducerList(self):
        iot_Producer_node_list = []
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTProducerHost):
                iot_Producer_node_list.append(node)
        return iot_Producer_node_list

    def remove_all_iot_devices(self):
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance(node, IoTProducerHost):
                #if i.NodeType == 'IoT_Device_Host':
                self.__stopAndRemoveContainers(node.NodeDockerRemoteClient)


    def remove_all_gateways(self):
        for node in self.parent_IoTNetwork.IoTNodeList:
            if isinstance (node, IoTGatewayHost):
                self.__stopAndRemoveContainers(node.NodeDockerRemoteClient)

    def __stopAndRemoveContainers(self,client_manager):

        # stop created containers
        for container in client_manager.containers.list (all):
            print ('Stopping container\t' + container.name)
            if container.status != 'running':
                container.remove ()
            else:
                container.kill ()
                container.remove ()


    def set_distribution_policy_balanced(self):
        self.distribution_policy = 'fill_first'


    def set_distribution_policy_random(self):
        self.set_distribution_policy_random = 'random'



    def get_free_IoTProducerHost(self):
        for found_node in self.parent_IoTNetwork.IoTNodeList:
            # check to see if the node is less than the max the edge can handle
            if isinstance(found_node, IoTProducerHost) and (self.__getContainerCount(found_node.NodeDockerRemoteClient) < found_node.max_allowed_iot_devices_on_this_host):
                #print('I found Producer node: ' + found_node.NodeName + 'it has a capacity of: ' +str(found_node.max_allowed_iot_devices_on_this_host))
                return found_node

    def __getContainerCount(self,client_manager):
        container_list = client_manager.containers.list (all)
        return len (container_list)

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



