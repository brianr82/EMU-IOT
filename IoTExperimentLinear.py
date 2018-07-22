from IoTExperiment import *


import docker
import time
import datetime


from IoTNode import *
from IoTMonitorManager import *
from IoTApplicationHost import *
from receiver import *
from IoTMonitor import *
from threading import Thread
from IoTDockerController import *
from SensorPair import *
from IoTNetwork import *
from IoTLoadBalancer import *
from IoTTemperatureGateway import *
from IoTCameraGateway import *
from IoTTemperatureSensor import *
from IoTDeviceType import *
from IoTDeviceService import *

import sys


class IoTExperimentLinear(IoTExperiment):
    def __init__(self):
        IoTExperiment.__init__(self)

        self.IoTLinearLoadbalancer = None
        self.IoTLinearMonitorManager = None



    def run(self):
        self.__configureNetwork()
        self.__configureMonitor()
        self.__executeWorkload()
        self.__cleanUp()


    def __configureNetwork(self):

        # configs for docker machine that will host the synthetic iot devices
        iot_producer_manager_docker_ip_1 = '10.12.7.50'
        iot_producer_manager_docker_port_1 = '2375'
        iot_producer_manager_docker_ip_2 = '10.12.7.51'
        iot_producer_manager_docker_port_2 = '2375'

        # configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
        iot_gateway_manager_docker_ip_1 = '10.12.7.52'
        iot_gateway_manager_docker_port_1 = '2375'
        iot_gateway_manager_docker_ip_2 = '10.12.7.53'
        iot_gateway_manager_docker_port_2 = '2375'

        # configs for docker machine that will host the kafka cluster
        kafka_manager_docker_ip = '10.12.7.48'
        kafka_manager_docker_port = '2375'
        # configs for docker machine that will host the spark instances
        spark_manager_docker_ip = '10.12.7.49'
        spark_manager_docker_port = '2375'
        # configs for docker machine that will host the assandra instances
        cassandra_manager_docker_ip = '10.12.7.5'
        cassandra_manager_docker_port = '2375'

        # Create remote docker clients to manage simulation environment
        iot_producer_client_1 = docker.DockerClient (
            base_url='tcp://' + iot_producer_manager_docker_ip_1 + ':' + iot_producer_manager_docker_port_1)
        iot_gateway_client_1 = docker.DockerClient (
            base_url='tcp://' + iot_gateway_manager_docker_ip_1 + ':' + iot_gateway_manager_docker_port_1)

        iot_producer_client_2 = docker.DockerClient (
            base_url='tcp://' + iot_producer_manager_docker_ip_2 + ':' + iot_producer_manager_docker_port_2)
        iot_gateway_client_2 = docker.DockerClient (
            base_url='tcp://' + iot_gateway_manager_docker_ip_2 + ':' + iot_gateway_manager_docker_port_2)

        kafka_client = docker.DockerClient (
            base_url='tcp://' + kafka_manager_docker_ip + ':' + kafka_manager_docker_port)
        spark_client = docker.DockerClient (
            base_url='tcp://' + spark_manager_docker_ip + ':' + spark_manager_docker_port)
        cassandra_client = docker.DockerClient (
            base_url='tcp://' + cassandra_manager_docker_ip + ':' + cassandra_manager_docker_port)

        # create a new IoT Network
        iot_network_1 = IoTNetwork ('Primary_Network')

        # create a new Iot Loadbalancer and assign it to the new network
        iot_lb_1 = IoTLoadBalancer ('LoadBalancer1', iot_network_1)

        # add nodes to the network
        # each node represents an instance of docker(i.e. a VM)
        iot_network_1.IoTNodeList.append (
            IoTApplicationHost ('Application', 'Kafka', kafka_client, kafka_manager_docker_ip,
                                kafka_manager_docker_port))
        iot_network_1.IoTNodeList.append (
            IoTApplicationHost ('Application', 'Spark', spark_client, spark_manager_docker_ip,
                                spark_manager_docker_port))
        iot_network_1.IoTNodeList.append (
            IoTApplicationHost ('Application', 'Cassandra', cassandra_client, cassandra_manager_docker_ip,
                                cassandra_manager_docker_port))
        iot_network_1.IoTNodeList.append (
            IoTProducerHost ('IoT_Device_Host', 'IoTProducer1', iot_producer_client_1, iot_producer_manager_docker_ip_1,
                             iot_producer_manager_docker_port_1))
        iot_network_1.IoTNodeList.append (
            IoTGatewayHost ('IoT_Gateway_Host', 'IoTReceiver1', iot_gateway_client_1, iot_gateway_manager_docker_ip_1,
                            iot_gateway_manager_docker_port_1))
        iot_network_1.IoTNodeList.append (
            IoTProducerHost ('IoT_Device_Host', 'IoTProducer2', iot_producer_client_2, iot_producer_manager_docker_ip_2,
                             iot_producer_manager_docker_port_2))
        iot_network_1.IoTNodeList.append (
            IoTGatewayHost ('IoT_Gateway_Host', 'IoTReceiver2', iot_gateway_client_2, iot_gateway_manager_docker_ip_2,
                            iot_gateway_manager_docker_port_2))

        # bind the IoTProducer to a gateway
        iot_lb_1.parent_IoTNetwork.get_IoTNode ('IoTProducer1').bindToIoTNode (
            iot_lb_1.parent_IoTNetwork.get_IoTNode ('IoTReceiver1'))
        iot_lb_1.parent_IoTNetwork.get_IoTNode ('IoTProducer2').bindToIoTNode (
            iot_lb_1.parent_IoTNetwork.get_IoTNode ('IoTReceiver2'))

        # Cleanup Old Containers from previous experiments
        iot_lb_1.iot_network_cleanup()

        #make the load balancer usable outside the method

        self.IoTLinearLoadbalancer = iot_lb_1


    def __configureMonitor(self):
        print (
            '*********************************************************************************************************')
        print ('Attempting to configure monitors')
        print (
            '*********************************************************************************************************')

        # set the name of this experiment run
        experiment_tag = self.ExperimentName
        # set the subdirectory name where you want the results data files to go
        directory = 'ExperimentResults/'
        '''
        print('Starting monitor for: '+ iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1').NodeName)
        PiMonitor = IoTMonitor(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1').NodeDockerRemoteClient)
        PiMonitor.create_new_result_file(directory+'PiReadings_'+ experiment_tag)
        Pi_thread = Thread(target=PiMonitor.createNewMonitor)

        print('Starting monitor for: '+ iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').NodeName)
        ProducerMonitor = IoTMonitor(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').NodeDockerRemoteClient)
        ProducerMonitor.create_new_result_file(directory+'Producer_Readings_'+experiment_tag)
        ProducerThread = Thread(target=ProducerMonitor.createNewMonitor)
        '''
        print ('Starting monitor for: ' + self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Kafka').NodeName)
        KafkaMonitor = IoTMonitor (self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Kafka').NodeDockerRemoteClient,
                                   IoTMonitorType.kafka)
        KafkaMonitor.create_new_result_file (directory + 'KafkaReadings_' + experiment_tag)
        Kafka_thread = Thread (target=KafkaMonitor.getUpdatedStats)

        print ('Starting monitor for: ' + self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Spark').NodeName)
        Spark_Monitor = IoTMonitor (self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Spark').NodeDockerRemoteClient,
                                    IoTMonitorType.spark)
        Spark_Monitor.create_new_result_file (directory + 'Spark_Readings_' + experiment_tag)
        Spark_Thread = Thread (target=Spark_Monitor.getUpdatedStats)

        print ('Starting monitor for: ' + self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Cassandra').NodeName)
        Cassandra_Monitor = IoTMonitor (self.IoTLinearLoadbalancer.parent_IoTNetwork.get_IoTNode ('Cassandra').NodeDockerRemoteClient,
                                        IoTMonitorType.cassandra)
        Cassandra_Monitor.create_new_result_file (directory + 'Cassandra_Readings_' + experiment_tag)
        Cassandra_Thread = Thread (target=Cassandra_Monitor.getUpdatedStats)

        # create the monitor manager
        MonitorManager = IoTMonitorManager ()
        # add the monitors
        # MonitorManager.addMonitor(PiMonitor)
        # MonitorManager.addMonitor(ProducerMonitor)
        #MonitorManager.addMonitor (Spark_Monitor)
        MonitorManager.addMonitor (KafkaMonitor)
        #MonitorManager.addMonitor (Cassandra_Monitor)

        # add the threads
        # MonitorManager.addThread(Pi_thread)
        # MonitorManager.addThread(ProducerThread)
        #MonitorManager.addThread (Spark_Thread)
        MonitorManager.addThread (Kafka_thread)
        #MonitorManager.addThread (Cassandra_Thread)

        print (
            '*********************************************************************************************************')
        print ('Experiment Monitors Configured')
        print (
            '*********************************************************************************************************')
        # make the monitor usable outside the method
        self.IoTLinearMonitorManager = MonitorManager









    def __executeWorkload(self):
        print (
            'Starting New Experiment Session..........................................................................')

        # Step 1: Create the virtual gateways

        # get list of all IotGatewayHostNodes (ie Vm's that can host VirtualIotGateway's)
        host_gateway_list = self.IoTLinearLoadbalancer.getIoTHostGatewayList ()

        # Gateway Host Configuration
        for gateway_host in host_gateway_list:

            # set the name of the Gateway Host
            receiver_prefix = gateway_host.NodeName + '_'
            # set the max number of virtual gateways you want on each gateway host
            gateway_host.maxNumberOfVirtualIoTGatewaysSupported = 4
            # set the max numbers of virtual IoT devices that can be assigned to a single virtual gateway
            max_number_iot_devices_supported_in_virtual_gateway = 50
            print ('Physical Gateway Host ' + gateway_host.NodeName + ' will support ' + str (
                gateway_host.maxNumberOfVirtualIoTGatewaysSupported * max_number_iot_devices_supported_in_virtual_gateway) + ' IoTdevices')

            start_remote_port_range = 3000
            end_remote_port_range = start_remote_port_range + gateway_host.maxNumberOfVirtualIoTGatewaysSupported

            for port_number in range (start_remote_port_range, end_remote_port_range):
                print ('Creating Temperature Gateway')
                # create the each virtual gateway
                new_iot_temperature_gateway = IoTTemperatureGateway (receiver_prefix + '_receiver_' + str (port_number),
                                                                     port_number,
                                                                     max_number_iot_devices_supported_in_virtual_gateway,
                                                                     gateway_host,
                                                                     IoTDeviceType.temperature)
                # create the actual docker container
                new_iot_temperature_gateway.createIoTVirtualGateway ()
                # register the  virtual gateway to the physical gateway host
                gateway_host.addVirtualGateway (new_iot_temperature_gateway)

                print ('Creating Camera Gateway')
                # create the each virtual gateway
                new_iot_camera_gateway = IoTCameraGateway (receiver_prefix + '_receiver_' + str (port_number + 10),
                                                           port_number + 10,
                                                           max_number_iot_devices_supported_in_virtual_gateway,
                                                           gateway_host, IoTDeviceType.camera)
                # create the actual docker container
                new_iot_camera_gateway.createIoTVirtualGateway ()
                # register the  virtual gateway to the physical gateway host
                gateway_host.addVirtualGateway (new_iot_camera_gateway)

        print ('---------------------------------Done creating IoTGateways')

        print ('---------------------------------Starting the monitors')
        self.IoTLinearMonitorManager.startAllMonitors()
        time.sleep (10)

        # Step 2: Create the virtual sensors
        '''
        SMART TESTING LINEAR INCREASE EXPERIMENT
        '''

        print ('---------------------------------Starting Linear Increase Experiment')

        DeviceService = IoTDeviceService()

        monitor_to_check = None
        target_cpu_percentage = self.TargetUtilization

        # loop through list and find the monitor you need
        for monitor in self.IoTLinearMonitorManager.IoTMonitorList:
            if monitor.MonitorType == self.ApplicationToMonitor:
                monitor_to_check = monitor

        reading_cycles = 3

        search_for_target_usage = True

        while (search_for_target_usage):

            if monitor_to_check.hostCPUUsage > target_cpu_percentage:
                # sleep for n seconds to get second reading to ignore spikes and try again
                print ('cpu threshold has been reached, but I will try ' + str (
                    reading_cycles) + ' cycles and check again to make sure')
                not_able_to_create = True
                for f in range (0, reading_cycles):
                    time.sleep (5)
                    if monitor_to_check.hostCPUUsage < target_cpu_percentage:
                        print (str (monitor_to_check.MonitorType) + ' usage is ' + str (
                            monitor_to_check.hostCPUUsage) + '% I can continue, was only a cpu blip')
                        DeviceService.addVirutalIoTDevice (self.IoTLinearLoadbalancer, IoTDeviceType.temperature, self.IoTLinearMonitorManager)
                        not_able_to_create = False
                        break

                if (not_able_to_create):
                    print (
                        'It has been verified, cpu threshold has been reached, I will not create more sensors, exiting')
                    break


            else:

                print (str (monitor_to_check.MonitorType) + ' usage is ' + str (
                    monitor_to_check.hostCPUUsage) + '% I can continue')

                # loop through list and find kafka monitor
                DeviceService.addVirutalIoTDevice (self.IoTLinearLoadbalancer, IoTDeviceType.temperature, self.IoTLinearMonitorManager)











    def __cleanUp(self):
        print ('Experiment over starting clean up')
        experiment_run_time_seconds = 3600
        time.sleep (experiment_run_time_seconds)
        print ('End Experiment')

        print ('Stopping Monitors')
        self.IoTLinearMonitorManager.stopAllMonitors ()

        # wait for all threads to finish before ending the program
        print ('Joining Monitor Threads')
        self.IoTLinearMonitorManager.joinThreads ()

        time.sleep (10)

        # kill the receivers after the experiment

        self.IoTLinearLoadbalancer.remove_all_gateways ()
        self.IoTLinearLoadbalancer.remove_all_iot_devices ()

        time.sleep (10)
