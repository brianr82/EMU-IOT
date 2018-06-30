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

import sys


#Run these on the respective docker machines
# docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
# docker build --no-cache=true -f latest/Dockerfile https://github.com/brianr82/node-red-docker.git -t brianr82/multinodered:latest

'''
*****************************************************************************************************************





Configuration Settings






*****************************************************************************************************************
'''

#configs for docker machine that will host the synthetic iot devices
iot_producer_manager_docker_ip_1 = '10.12.7.50'
iot_producer_manager_docker_port_1 = '2375'
iot_producer_manager_docker_ip_2 = '10.12.7.51'
iot_producer_manager_docker_port_2 = '2375'

#configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
iot_gateway_manager_docker_ip_1 = '10.12.7.52'
iot_gateway_manager_docker_port_1 = '2375'
iot_gateway_manager_docker_ip_2 = '10.12.7.53'
iot_gateway_manager_docker_port_2 = '2375'


#configs for docker machine that will host the kafka cluster
kafka_manager_docker_ip = '10.12.7.48'
kafka_manager_docker_port = '2375'
#configs for docker machine that will host the spark instances
spark_manager_docker_ip = '10.12.7.49'
spark_manager_docker_port = '2375'
#configs for docker machine that will host the assandra instances
cassandra_manager_docker_ip = '10.12.7.5'
cassandra_manager_docker_port = '2375'


#Create remote docker clients to manage simulation environment
iot_producer_client_1 = docker.DockerClient(base_url='tcp://'+iot_producer_manager_docker_ip_1+':'+iot_producer_manager_docker_port_1)
iot_gateway_client_1 = docker.DockerClient(base_url='tcp://'+iot_gateway_manager_docker_ip_1+':'+iot_gateway_manager_docker_port_1)

iot_producer_client_2 = docker.DockerClient(base_url='tcp://'+iot_producer_manager_docker_ip_2+':'+iot_producer_manager_docker_port_2)
iot_gateway_client_2 = docker.DockerClient(base_url='tcp://'+iot_gateway_manager_docker_ip_2+':'+iot_gateway_manager_docker_port_2)

kafka_client = docker.DockerClient(base_url='tcp://'+kafka_manager_docker_ip+':'+kafka_manager_docker_port)
spark_client = docker.DockerClient(base_url='tcp://'+spark_manager_docker_ip+':'+spark_manager_docker_port)
cassandra_client = docker.DockerClient(base_url='tcp://'+cassandra_manager_docker_ip+':'+cassandra_manager_docker_port)




#create a new IoT Network
iot_network_1 = IoTNetwork('Primary_Network')

#create a new Iot Loadbalancer and assign it to the new network
iot_lb_1 = IoTLoadBalancer('LoadBalancer1',iot_network_1)

#add nodes to the network
#each node represents an instance of docker(i.e. a VM)
iot_network_1.IoTNodeList.append(IoTApplicationHost('Application','Kafka',kafka_client,kafka_manager_docker_ip,kafka_manager_docker_port))
iot_network_1.IoTNodeList.append(IoTApplicationHost('Application','Spark',spark_client,spark_manager_docker_ip,spark_manager_docker_port))
iot_network_1.IoTNodeList.append(IoTApplicationHost('Application','Cassandra',cassandra_client,cassandra_manager_docker_ip,cassandra_manager_docker_port))
iot_network_1.IoTNodeList.append(IoTProducerHost('IoT_Device_Host','IoTProducer1',iot_producer_client_1,iot_producer_manager_docker_ip_1,iot_producer_manager_docker_port_1))
iot_network_1.IoTNodeList.append(IoTGatewayHost('IoT_Gateway_Host','IoTReceiver1',iot_gateway_client_1,iot_gateway_manager_docker_ip_1,iot_gateway_manager_docker_port_1))
iot_network_1.IoTNodeList.append(IoTProducerHost('IoT_Device_Host','IoTProducer2',iot_producer_client_2,iot_producer_manager_docker_ip_2,iot_producer_manager_docker_port_2))
iot_network_1.IoTNodeList.append(IoTGatewayHost('IoT_Gateway_Host','IoTReceiver2',iot_gateway_client_2,iot_gateway_manager_docker_ip_2,iot_gateway_manager_docker_port_2))



#bind the IoTProducer to a gateway
iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').bindToIoTNode(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1'))
iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer2').bindToIoTNode(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver2'))

#Cleanup Old Containers from previous experiments
iot_lb_1.iot_network_cleanup()



'''
*****************************************************************************************************************





Experiment Monitors





*****************************************************************************************************************
'''
print('*********************************************************************************************************')
print('Attempting to start monitors')
print('*********************************************************************************************************')

#set the name of this experiment run
experiment_tag = 'Run_1_Final_Test'
#set the subdirectory name where you want the results data files to go
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
print('Starting monitor for: '+ iot_lb_1.parent_IoTNetwork.get_IoTNode('Kafka').NodeName)
KafkaMonitor = IoTMonitor(iot_lb_1.parent_IoTNetwork.get_IoTNode('Kafka').NodeDockerRemoteClient)
KafkaMonitor.create_new_result_file(directory+'KafkaReadings_'+ experiment_tag)
Kafka_thread = Thread(target=KafkaMonitor.getUpdatedStats)

print('Starting monitor for: '+ iot_lb_1.parent_IoTNetwork.get_IoTNode('Spark').NodeName)
Spark_Monitor = IoTMonitor(iot_lb_1.parent_IoTNetwork.get_IoTNode('Spark').NodeDockerRemoteClient)
Spark_Monitor.create_new_result_file(directory+'Spark_Readings_'+ experiment_tag)
Spark_Thread = Thread(target=Spark_Monitor.getUpdatedStats)

print('Starting monitor for: '+ iot_lb_1.parent_IoTNetwork.get_IoTNode('Cassandra').NodeName)
Cassandra_Monitor = IoTMonitor(iot_lb_1.parent_IoTNetwork.get_IoTNode('Cassandra').NodeDockerRemoteClient)
Cassandra_Monitor.create_new_result_file(directory+'Cassandra_Readings_'+ experiment_tag)
Cassandra_Thread = Thread(target=Cassandra_Monitor.getUpdatedStats)

#create the monitor manager
MonitorManager = IoTMonitorManager()
#add the monitors
#MonitorManager.addMonitor(PiMonitor)
#MonitorManager.addMonitor(ProducerMonitor)
MonitorManager.addMonitor(Spark_Monitor)
MonitorManager.addMonitor(KafkaMonitor)
MonitorManager.addMonitor(Cassandra_Monitor)

#add the threads
#MonitorManager.addThread(Pi_thread)
#MonitorManager.addThread(ProducerThread)
MonitorManager.addThread(Kafka_thread)
MonitorManager.addThread(Spark_Thread)
MonitorManager.addThread(Cassandra_Thread)


print('*********************************************************************************************************')
print('Experiment Monitors Started')
print('*********************************************************************************************************')
'''
******************************************************************************************************************












Main Program














******************************************************************************************************************
'''
'''
Experiment Workload Distributed***********************************************************************************
'''

def workloadDist():
    print('Starting New Experiment Session..........................................................................')
    MonitorManager.startAllMonitors()

    # Step 1: Create the virtual gateways


    #get list of all IotGatewayHostNodes (ie Vm's that can host VirtualIotGateway's)
    host_gateway_list = iot_lb_1.getIoTHostGatewayList()


    #Gateway Host Configuration
    for gateway_host in host_gateway_list:

        #set the name of the Gateway Host
        receiver_prefix = gateway_host.NodeName + '_'
        # set the max number of virtual gateways you want on each gateway host
        gateway_host.maxNumberOfVirtualIoTGatewaysSupported =4
        #set the max numbers of virtual IoT devices that can be assigned to a single virtual gateway
        max_number_iot_devices_supported_in_virtual_gateway = 50
        print('Physical Gateway Host ' + gateway_host.NodeName + ' will support '+ str(gateway_host.maxNumberOfVirtualIoTGatewaysSupported*max_number_iot_devices_supported_in_virtual_gateway) +' IoTdevices')

        start_remote_port_range = 3000
        end_remote_port_range = start_remote_port_range + gateway_host.maxNumberOfVirtualIoTGatewaysSupported




        for port_number in range(start_remote_port_range, end_remote_port_range):


            print ('Creating Temperature Gateway')
            #create the each virtual gateway
            new_iot_temperature_gateway = IoTTemperatureGateway(receiver_prefix + '_receiver_' + str(port_number),
                                                                port_number,
                                                                max_number_iot_devices_supported_in_virtual_gateway,
                                                                gateway_host,
                                                                IoTDeviceType.temperature)
            #create the actual docker container
            new_iot_temperature_gateway.createIoTVirtualGateway()
            #register the  virtual gateway to the physical gateway host
            gateway_host.addVirtualGateway(new_iot_temperature_gateway)

            print ('Creating Camera Gateway')
            # create the each virtual gateway
            new_iot_camera_gateway = IoTCameraGateway (receiver_prefix + '_receiver_' + str (port_number+10),
                                                                 port_number+10,
                                                                 max_number_iot_devices_supported_in_virtual_gateway,
                                                                 gateway_host, IoTDeviceType.camera)
            # create the actual docker container
            new_iot_camera_gateway.createIoTVirtualGateway ()
            # register the  virtual gateway to the physical gateway host
            gateway_host.addVirtualGateway(new_iot_camera_gateway)

    print ('---------------------------------Done creating IoTGateways')

    # Step 2: Create the virtual sensors
    createNewSensor(400)










def createNewSensor(count):


    for producer_seq in range (1, count):

        producer_prefix = 'simsensor_' + str(producer_seq) +'_'
        number_of_msg_to_send = 10000000
        producer_device_delay = 1000000


        destination_producer_host = iot_lb_1.get_target_iot_device_edge('create')
        IoTProducerBinding = destination_producer_host
        IoTDeviceID =  'test'
        BoundIoTVirtualGateway = destination_producer_host.boundNode.getNextFreeVirtualGateway(IoTDeviceType.temperature)
        IoTDeviceName = destination_producer_host.NodeName + '_' +producer_prefix + str(BoundIoTVirtualGateway.gateway_app_port)



        new_sensor = IoTTemperatureSensor(IoTDeviceID,IoTDeviceName,IoTProducerBinding,number_of_msg_to_send,producer_device_delay)

        new_sensor.createVirtualIoTSensor()

        #add device to producer host
        IoTProducerBinding.addVirtualIoTDevice(new_sensor,BoundIoTVirtualGateway)

        #update the monitor
        MonitorManager.updateActiveProducerCount(iot_lb_1)



'''
Workload B ************************************************************************************************************


def workloadB():


    sensor_pair_list = []


    scaling_factor = 1


    number_of_receivers = 5 * scaling_factor
    number_of_sensors = 90 * scaling_factor
    number_of_sensors_assigned_to_receiver = number_of_sensors / number_of_receivers

    start_remote_port_range = 3000
    end_remote_port_range = start_remote_port_range + number_of_receivers

    receiver_prefix = 'receiver_'
    producer_prefix = 'simsensor_'

    receiver_list = []

    for port_number in range(start_remote_port_range, end_remote_port_range):
        receiver_name = receiver_prefix + str(port_number)
        r = receiver(receiver_name, port_number)
        receiver_list.append(r)
        for suffix_id in range(1, int(number_of_sensors_assigned_to_receiver) + 1):
            producer_name = producer_prefix + str(port_number) + '_' + str(suffix_id)
            sensor_pair_list.append(Sensorpair(port_number, producer_name, receiver_name,iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').boundNode.NodeIPAddress))

    #create all the receivers
    for r in receiver_list:
        createReceiverNew(receiver_client,r)
        time.sleep(5)

    time.sleep(10)





    
    Define workload profile below
    
    create the producers as needed

    number_of_msg_to_send = 10000000
    producer_device_delay = 1000000

    #Step 1_A - Create sensor pairs in batches of 15 every 3 minutes for 18 minutes (sleep for 60 x 3 = 180 seconds)

    pair_index = 0 #maintain the already created sensor pairs through all loop levels
    for x in range(0,6): # creating 6 batches of 15 so we will have 90 sensors
        for i in range(0,15*scaling_factor):
            new_sensor_pair = sensor_pair_list[pair_index]
            createProducerNew(producer_client,new_sensor_pair,number_of_msg_to_send,producer_device_delay)
            IoTMonitorManager.updateActiveProducerCount (iot_lb_1.get_current_iot_device_count ())
            pair_index +=1
        time.sleep(180) #wait 3 minutes(180 seconds) in between batches

    #Step 1_B stop the containers  in batches of 15 every 10 seconds
    for x in range(0, 6):
        stop_N_Producer_Containers(producer_client, MonitorManager.IoTMonitorList,15*scaling_factor)
        time.sleep(180) #wait 3 minutes(180 seconds) in between batches




    #Step 2_A Surge all 90 containers at once
    for pair_index in range(0, len(sensor_pair_list)):  #
        new_sensor_pair = sensor_pair_list[pair_index]
        createProducerNew(producer_client, new_sensor_pair, number_of_msg_to_send, producer_device_delay)
        IoTMonitorManager.updateActiveProducerCount (iot_lb_1.get_current_iot_device_count ())

        # time.sleep(180) #wait 3 minutes(180 seconds) in between batches

    time.sleep(540) #wait 9 minutes(540 seconds) in between batches

    #Step 2_B Stop 30 producers every 5 minutes
    for x in range(0, 6):
        stop_N_Producer_Containers(producer_client, MonitorManager.IoTMonitorList,30*scaling_factor)
        time.sleep(300)



'''


'''
End of Workload Profile B*****************************************************************************************
'''
'''
Call the workloads ************************************************************************************************
'''



#workloadB()
workloadDist()



'''
*****************************************************************************************************
Clean up
*****************************************************************************************************
'''
experiment_run_time_seconds = 90
time.sleep(experiment_run_time_seconds)
print ('End Experiment')



print ('Stopping Monitors')
MonitorManager.stopAllMonitors()


#wait for all threads to finish before ending the program
print ('Joining Monitor Threads')
MonitorManager.joinThreads()



time.sleep(10)




#kill the receivers after the experiment

iot_lb_1.remove_all_gateways()
iot_lb_1.remove_all_iot_devices()

time.sleep(10)






print ('-----------------------------Done')

sys.exit(0)