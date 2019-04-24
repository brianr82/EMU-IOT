from IoTExperiment import *


import docker

from IoTMonitorManager import *
from IoTApplicationHost import *
from IoTMonitor import *
from threading import Thread
#from OLD.IoTDockerController import *
from IoTLoadBalancer import *
from IoTTemperatureGateway import *
from IoTCameraGateway import *
#from IoTDeviceService import *
from IoTDeviceServiceTemperature import *
from IoTDeviceServiceCamera import *
from IoTMonitorType import *
from Regression import *


class IoTExperimentLinearRegression(IoTExperiment):
    def __init__(self):
        IoTExperiment.__init__(self)

        self.IoTLinearRegressionLoadbalancer = None
        self.IoTLinearRegressionMonitorManager = None
        self.DeviceServiceTemperature = None
        self.DeviceServiceCamera = None
        self.monitor_to_check = None
        self.TestCaseCompleted = True
        self.TestCaseCounter = 0
        self.current_active_producers = 0
        self.target_active_producers = 0


        #test case configs
        #self.temperature_sensors_per_test_case = 0
        #self.camera_sensors_per_test_case = 0




    def run(self):
        self.__resetCounters()
        self.__configureNetwork()
        self.__configureMonitor()
        self.__IoTNodeSetup()
        self.__startMonitors()
        self.__executeWorkload()
        self.__cleanUp()
        print ('Experiment Finished')

    def __resetCounters(self):
        self.TestCaseCounter = 0
        self.current_active_producers = 0
        self.target_active_producers = 0

    def configureExperiment(self,experiment_type):

        if experiment_type == 'temperature':
            self.temperature_sensors_per_test_case = int(round(Regression('training_data/temperature_only').getGenerateTestCase(self.targetCPUUtilization)))
            self.camera_sensors_per_test_case = 0

            print('Experiment Set to temperature sensors only')
            self.setApplicationToMonitor(IoTMonitorType.kafka)


        if experiment_type == 'camera':
            self.temperature_sensors_per_test_case = 0
            self.camera_sensors_per_test_case = int(round(Regression('training_data/camera_only').getGenerateTestCase(self.targetCPUUtilization)))

            print('Experiment Set to camera sensors only')
            self.setApplicationToMonitor(IoTMonitorType.cassandra)

        if experiment_type == 'mix':
            self.temperature_sensors_per_test_case = int(round(10/11 * Regression('training_data/mix').getGenerateTestCase(self.targetCPUUtilization)))
            print('Number of temperature sensors: ' + str(self.temperature_sensors_per_test_case))
            self.camera_sensors_per_test_case = int(round(1/11 * Regression('training_data/mix').getGenerateTestCase(self.targetCPUUtilization)))
            print ('Number of camera sensors: ' + str(self.camera_sensors_per_test_case))

            print('Experiment Set to 1 camera + 10 temperature sensors')
            self.setApplicationToMonitor(IoTMonitorType.kafka)


    def __configureNetwork(self):

        # configs for docker machine that will host the synthetic iot devices
        iot_producer_manager_docker_ip_1 = '10.12.7.62'
        iot_producer_manager_docker_port_1 = '2375'
        iot_producer_manager_docker_ip_2 = '10.12.7.63'
        iot_producer_manager_docker_port_2 = '2375'

        # configs for docker machine that will host the receiver gateway(Pi) that has a connection to temperature_only
        iot_gateway_manager_docker_ip_1 = '10.12.7.67'
        iot_gateway_manager_docker_port_1 = '2375'
        iot_gateway_manager_docker_ip_2 = '10.12.7.68'
        iot_gateway_manager_docker_port_2 = '2375'

        # configs for docker machine that will host the temperature_only cluster
        kafka_manager_docker_ip = '10.12.7.64'
        kafka_manager_docker_port = '2375'
        # configs for docker machine that will host the spark instances
        spark_manager_docker_ip = '10.12.7.65'
        spark_manager_docker_port = '2375'
        # configs for docker machine that will host the assandra instances
        cassandra_manager_docker_ip = '10.12.7.66'
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

        self.IoTLinearRegressionLoadbalancer = iot_lb_1


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
        print ('Starting monitor for: ' + self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Kafka').NodeName)
        KafkaMonitor = IoTMonitor (self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Kafka').NodeDockerRemoteClient,
                                   IoTMonitorType.kafka)
        KafkaMonitor.create_new_result_file (directory + 'KafkaReadings_' + experiment_tag +'.txt')
        Kafka_thread = Thread (target=KafkaMonitor.getUpdatedStats)

        #print ('Starting monitor for: ' + self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Spark').NodeName)
        #Spark_Monitor = IoTMonitor (self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Spark').NodeDockerRemoteClient, IoTMonitorType.spark)
        #Spark_Monitor.create_new_result_file (directory + 'Spark_Readings_' + experiment_tag +'.txt')
        #Spark_Thread = Thread (target=Spark_Monitor.getUpdatedStats)

        #print ('Starting monitor for: ' + self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Cassandra').NodeName)
        #Cassandra_Monitor = IoTMonitor (self.IoTLinearRegressionLoadbalancer.parent_IoTNetwork.get_IoTNode ('Cassandra').NodeDockerRemoteClient, IoTMonitorType.cassandra)
        #Cassandra_Monitor.create_new_result_file (directory + 'Cassandra_Readings_' + experiment_tag +'.txt')
        #Cassandra_Thread = Thread (target=Cassandra_Monitor.getUpdatedStats)

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
        self.IoTLinearRegressionMonitorManager = MonitorManager

        # set the monitor that you want to use to find the bottleneck
        # loop through list and find the monitor you need
        for monitor in self.IoTLinearRegressionMonitorManager.IoTMonitorList:
            if monitor.MonitorType == self.ApplicationToMonitor:
                self.monitor_to_check = monitor
                print(monitor.MonitorType)



    def __IoTNodeSetup(self):
        print ('............................................Configuring producer hosts and activating virtual gateways')
        # Step 1: Configure Producer Hosts
        host_producer_list = self.IoTLinearRegressionLoadbalancer.getIoTHostProducerList ()
        for producer_host in host_producer_list:
            producer_host.max_allowed_iot_devices_on_this_host = self.max_devices_on_a_producer_host

        # Step 2: Create the virtual gateways

        max_VirtualIoTGatewaysSupportedOnAGatewayHost = self.max_devices_on_a_producer_host // self.max_devices_assigned_to_a_virtual_gateway

        # get list of all IotGatewayHostNodes (ie Vm's that can host VirtualIotGateway's)
        host_gateway_list = self.IoTLinearRegressionLoadbalancer.getIoTHostGatewayList ()

        # Gateway Host Configuration
        for gateway_host in host_gateway_list:

            # set the name of the Gateway Host
            receiver_prefix = gateway_host.NodeName + '_'
            # set the max number of virtual gateways you want on each gateway host
            gateway_host.maxNumberOfVirtualIoTGatewaysSupported = max_VirtualIoTGatewaysSupportedOnAGatewayHost
            # set the max numbers of virtual IoT devices that can be assigned to a single virtual gateway
            max_number_iot_devices_supported_in_virtual_gateway = self.max_devices_assigned_to_a_virtual_gateway
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

                #start the Device Service
                self.DeviceServiceTemperature = IoTDeviceServiceTemperature()
                self.DeviceServiceCamera = IoTDeviceServiceCamera()

        print('.....................................Done configuring producer hosts and creating Virtual IoT Gateways')


    def __startMonitors(self):
        print ('........................................................................Starting New Experiment Session')
        print ('..................................................................................Starting the monitors')
        self.IoTLinearRegressionMonitorManager.startAllMonitors()
        time.sleep (10)


    def __executeWorkload(self):
        print ('...................................................................Starting Linear Regression Experiment')
        #step 1: create all the sensors
        self.__generateTestCase ()
        #step 2: wait for 60 seconds to get more readings
        time.sleep (60)


    def __generateTestCase(self):
        #check to see if previous test case has been completed, if so we can create a new one
        print ('Checking to see if previous test case was completed')
        if self.TestCaseCompleted == True:
            print ('Previous Test case was completed, starting a new one')

            #set the goal state to false because we are about to change the active producer target
            self.TestCaseCompleted = False

            '''Generate Temperature Sensors'''
            for i in range(0,self.temperature_sensors_per_test_case):
                self.DeviceServiceTemperature.addVirutalIoTDevice (self.IoTLinearRegressionLoadbalancer,self.IoTLinearRegressionMonitorManager)
                self.target_active_producers = self.target_active_producers + 1
            '''Generate Camera Sensors'''
            for i in range (0, self.camera_sensors_per_test_case):
                self.DeviceServiceCamera.addVirutalIoTDevice (self.IoTLinearRegressionLoadbalancer, self.IoTLinearRegressionMonitorManager)
                self.target_active_producers = self.target_active_producers + 1

            self.TestCaseCounter =  self.TestCaseCounter + 1
            self.current_active_producers = self.monitor_to_check.ActiveProducers


        #previous test case has not completed, we sleep and the caller of this function will check try again later to generate a test case
        else:
            if self.current_active_producers != self.target_active_producers:
                # wait for time time until the previous test case has been completed
                print ('Previous Test case has NOT yet completed, sleeping for 5 seconds')
                time.sleep(5)
                self.current_active_producers = self.monitor_to_check.ActiveProducers
                #if self.current_active_producers == self.target_active_producers:
                #    self.TestCaseCompleted == True

                print('Current Active Producers '+str(self.current_active_producers))
                print('Target Active Producers ' + str(self.target_active_producers))
                print('Monitor Active Producers ' + str(self.monitor_to_check.ActiveProducers))

            if self.current_active_producers == self.target_active_producers:
                #the current goal is the same as the target goal, the test case is complete, set the flag
                print ('The number of active producers is equal to the number of target producers, the test case was completed sucessfully')
                print ('Current Active Producers ' + str (self.current_active_producers))
                print ('Target Active Producers ' + str (self.target_active_producers))
                print ('Monitor Active Producers ' + str (self.monitor_to_check.ActiveProducers))
                self.TestCaseCompleted = True






    def __cleanUp(self):
        print ('Experiment over starting clean up')
        print ('Number of Test Cases Required to Reach Target: ' + str(self.TestCaseCounter))
        experiment_shutdown_delay_seconds = 20
        time.sleep (experiment_shutdown_delay_seconds)
        print ('End Experiment')

        print ('Stopping Monitors')
        self.IoTLinearRegressionMonitorManager.stopAllMonitors ()

        # wait for all threads to finish before ending the program
        print ('Joining Monitor Threads')
        self.IoTLinearRegressionMonitorManager.joinThreads ()

        time.sleep (10)

        # kill the receivers after the experiment


        #self.IoTLinearLoadbalancer.remove_all_iot_devices ()
        temperature_devices_to_remove = True
        while temperature_devices_to_remove:
            temperature_devices_to_remove = self.DeviceServiceTemperature.removeVirtualIoTDevice(self.IoTLinearRegressionLoadbalancer,self.IoTLinearRegressionMonitorManager)

        camera_devices_to_remove = True
        while camera_devices_to_remove:
            camera_devices_to_remove = self.DeviceServiceCamera.removeVirtualIoTDevice(self.IoTLinearRegressionLoadbalancer,self.IoTLinearRegressionMonitorManager)

        self.IoTLinearRegressionLoadbalancer.remove_all_gateways ()

        time.sleep (10)
