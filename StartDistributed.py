import docker
import time
import datetime


from IoTNode import *

from IoTApplicationHost import *
from receiver import *
from IoTMonitor import *
from threading import Thread
from IoTDockerController import *
from SensorPair import *
from IoTNetwork import *
from IoTLoadBalancer import *
from IoTVirtualGateway import *
from IoTTemperatureSensor import *
import sys


#Run these on the respective docker machines
# docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
# docker build --no-cache=true -f latest/Dockerfile https://github.com/brianr82/node-red-docker.git -t brianr82/multinodered:latest

'''
Configs
'''

#configs for docker machine that will host the synthetic iot devices
iot_producer_manager_docker_ip_1 = '192.168.2.240'
iot_producer_manager_docker_port_1 = '2375'
iot_producer_manager_docker_ip_2 = '192.168.2.241'
iot_producer_manager_docker_port_2 = '2375'

#configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
iot_gateway_manager_docker_ip_1 = '192.168.2.242'
iot_gateway_manager_docker_port_1 = '2375'
iot_gateway_manager_docker_ip_2 = '192.168.2.243'
iot_gateway_manager_docker_port_2 = '2375'


#configs for docker machine that will host the kafka cluster
kafka_manager_docker_ip = '10.12.7.41'
kafka_manager_docker_port = '2375'
#configs for docker machine that will host the spark_cassandra instances
spark_cassandra_manager_docker_ip = '10.12.7.42'
spark_cassandra_manager_docker_port = '2375'



#Create remote docker clients to manage simulation environment
iot_producer_client_1 = docker.DockerClient(base_url='tcp://'+iot_producer_manager_docker_ip_1+':'+iot_producer_manager_docker_port_1)
iot_gateway_client_1 = docker.DockerClient(base_url='tcp://'+iot_gateway_manager_docker_ip_1+':'+iot_gateway_manager_docker_port_1)

iot_producer_client_2 = docker.DockerClient(base_url='tcp://'+iot_producer_manager_docker_ip_2+':'+iot_producer_manager_docker_port_2)
iot_gateway_client_2 = docker.DockerClient(base_url='tcp://'+iot_gateway_manager_docker_ip_2+':'+iot_gateway_manager_docker_port_2)

kafka_client = docker.DockerClient(base_url='tcp://'+kafka_manager_docker_ip+':'+kafka_manager_docker_port)
spark_cassandra_client = docker.DockerClient(base_url='tcp://'+spark_cassandra_manager_docker_ip+':'+spark_cassandra_manager_docker_port)




#create a new IoT Network
iot_network_1 = IoTNetwork('Primary_Network')

#create a new Iot Loadbalancer and assign it to the new network
iot_lb_1 = IoTLoadBalancer('LoadBalancer1',iot_network_1)

#add nodes to the network
#each node represents an instance of docker(i.e. a VM)
iot_network_1.IoTNodeList.append(IoTApplicationHost('Application','Kafka01',kafka_client,kafka_manager_docker_ip,kafka_manager_docker_port))
iot_network_1.IoTNodeList.append(IoTApplicationHost('Application','SparkCassandra',spark_cassandra_client,spark_cassandra_manager_docker_ip,spark_cassandra_manager_docker_port))
iot_network_1.IoTNodeList.append(IoTProducerHost('IoT_Device_Host','IoTProducer1',iot_producer_client_1,iot_producer_manager_docker_ip_1,iot_producer_manager_docker_port_1))
iot_network_1.IoTNodeList.append(IoTGatewayHost('IoT_Gateway_Host','IoTReceiver1',iot_gateway_client_1,iot_gateway_manager_docker_ip_1,iot_gateway_manager_docker_port_1))
iot_network_1.IoTNodeList.append(IoTProducerHost('IoT_Device_Host','IoTProducer2',iot_producer_client_2,iot_producer_manager_docker_ip_2,iot_producer_manager_docker_port_2))
iot_network_1.IoTNodeList.append(IoTGatewayHost('IoT_Gateway_Host','IoTReceiver2',iot_gateway_client_2,iot_gateway_manager_docker_ip_2,iot_gateway_manager_docker_port_2))



#bind the IoTProducer to a gateway
iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').bindToIoTNode(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1'))
iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer2').bindToIoTNode(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver2'))

#Cleanup Old Containers from previous experiments
iot_lb_1.iot_network_cleanup()

#TO BE REMOVED
producer_client = iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').NodeDockerRemoteClient
receiver_client = iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1').NodeDockerRemoteClient

'''
*****************************************************************************************************************
Experiment Monitors
*****************************************************************************************************************
'''

'''
Start the monitors
'''

experiment_tag = 'Run_1_second_test_a'
directory = 'ExperimentResults/'


PiMonitor = monitor2(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTReceiver1').NodeDockerRemoteClient)
PiMonitor.create_new_result_file(directory+'PiReadings_'+ experiment_tag)
Pi_thread = Thread(target=PiMonitor.createNewMonitor)

Pi_thread.start()


KafkaMonitor = monitor2(iot_lb_1.parent_IoTNetwork.get_IoTNode('Kafka01').NodeDockerRemoteClient)
KafkaMonitor.create_new_result_file(directory+'KafkaReadings_'+ experiment_tag)
kafka_thread = Thread(target=KafkaMonitor.createNewMonitor)

kafka_thread.start()


ProducerMonitor = monitor2(iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').NodeDockerRemoteClient)
ProducerMonitor.create_new_result_file(directory+'Producer_Readings_'+experiment_tag)
producerThread = Thread(target=ProducerMonitor.createNewMonitor)

producerThread.start()


Spark_Cassandra_Monitor = monitor2(iot_lb_1.parent_IoTNetwork.get_IoTNode('SparkCassandra').NodeDockerRemoteClient)
Spark_Cassandra_Monitor.create_new_result_file(directory+'Spark_Cassandra_Readings_'+ experiment_tag)
Spark_Cassandra_Thread = Thread(target=Spark_Cassandra_Monitor.createNewMonitor)

Spark_Cassandra_Thread.start()



Monitor_list = []

Monitor_list.append(PiMonitor)
Monitor_list.append(KafkaMonitor)
Monitor_list.append(ProducerMonitor)
Monitor_list.append(Spark_Cassandra_Monitor)


def update_monitor():
    for m in Monitor_list:
        m.set_active_producer_count(iot_lb_1.get_current_iot_device_count())



print '*********************************************************************************************************'
print 'Starting New Experiment Session..........................................................................'
print 'Monitors Started'
print '*********************************************************************************************************'


'''
*****************************************************************************************************************
Main Program
*****************************************************************************************************************
'''

'''
Start the Producer and Receiver Containers
'''

'''
def workloadTest():
    start_remote_port_range = 2000
    number_of_sensor_receiver_pairs = 2
    end_remote_port_range = start_remote_port_range + number_of_sensor_receiver_pairs

    number_of_msg_to_send = 1000
    producer_device_delay = 500000

    for port_num in range(start_remote_port_range, end_remote_port_range):
        createSensorPair(receiver_client,producer_client,receiver_manager_docker_ip,port_num,number_of_msg_to_send,producer_device_delay,KafkaMonitor,ProducerMonitor,Spark_Cassandra_Monitor,PiMonitor)


Workload A ************************************************************************************************************
'''












'''
Workload Distributed***************************************************************************************************
'''





def workloadDist():
    # Step 1: Create the virtual gateways
    scaling_factor = 1

    number_of_receivers = 5 * scaling_factor
    number_of_sensors = 90 * scaling_factor
    number_of_sensors_assigned_to_receiver = number_of_sensors / number_of_receivers

    start_remote_port_range = 3000
    end_remote_port_range = start_remote_port_range + number_of_receivers


    #get list of all IotGatewayHostNodes (ie Vm's that can host VirtualIotGateway's)
    host_gateway_list = iot_lb_1.getIoTHostGatewayList()

    for gateway in host_gateway_list:
        receiver_prefix = gateway.NodeName + '_'

        for port_number in range(start_remote_port_range, end_remote_port_range):
            #create the each virtual gateway
            new_iotgateway = IoTVirtualGateway(receiver_prefix + '_receiver_' + str(port_number),port_number,5,gateway)
            #create the actual docker container
            new_iotgateway.createIoTVirtualGateway()
            #register the  virtual gateway to the physical gateway host
            gateway.addVirtualGateway(new_iotgateway)




    # Step 2: Create the virtual sensors
    createNewSensor(7)


def createNewSensor(count):


    for producer_seq in range (1, count):

        producer_prefix = 'simsensor_' + str(producer_seq) +'_'
        number_of_msg_to_send = 10000000
        producer_device_delay = 1000000


        destination_producer_host = iot_lb_1.get_target_iot_device_edge('create')
        IoTDeviceID =  'test'
        IoTDeviceName = destination_producer_host.NodeName + '_' +producer_prefix + str(destination_producer_host.boundNode.getNextFreeVirtualGateway().gateway_app_port)
        IoTProducerBinding = destination_producer_host


        new_sensor = IotTemperatureSensor(IoTDeviceID,IoTDeviceName,IoTProducerBinding,number_of_msg_to_send,producer_device_delay)

        new_sensor.createIoTVirtualTemperatureSensor()

        IoTProducerBinding.addVirtualIoTDevice(new_sensor)


'''
Workload B ************************************************************************************************************
'''

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
        for suffix_id in range(1, number_of_sensors_assigned_to_receiver + 1):
            producer_name = producer_prefix + str(port_number) + '_' + str(suffix_id)
            sensor_pair_list.append(Sensorpair(port_number, producer_name, receiver_name,iot_lb_1.parent_IoTNetwork.get_IoTNode('IoTProducer1').boundNode.NodeIPAddress))

    #create all the receivers
    for r in receiver_list:
        createReceiverNew(receiver_client,r)
        time.sleep(5)

    time.sleep(10)





    '''
    Define workload profile below
    '''
    #create the producers as needed

    number_of_msg_to_send = 10000000
    producer_device_delay = 1000000

    #Step 1_A - Create sensor pairs in batches of 15 every 3 minutes for 18 minutes (sleep for 60 x 3 = 180 seconds)

    pair_index = 0 #maintain the already created sensor pairs through all loop levels
    for x in range(0,6): # creating 6 batches of 15 so we will have 90 sensors
        for i in range(0,15*scaling_factor):
            new_sensor_pair = sensor_pair_list[pair_index]
            createProducerNew(producer_client,new_sensor_pair,number_of_msg_to_send,producer_device_delay)
            update_monitor()
            pair_index +=1
        time.sleep(180) #wait 3 minutes(180 seconds) in between batches

    #Step 1_B stop the containers  in batches of 15 every 10 seconds
    for x in range(0, 6):
        stop_N_Producer_Containers(producer_client, Monitor_list,15*scaling_factor)
        time.sleep(180) #wait 3 minutes(180 seconds) in between batches




    #Step 2_A Surge all 90 containers at once
    for pair_index in range(0, len(sensor_pair_list)):  #
        new_sensor_pair = sensor_pair_list[pair_index]
        createProducerNew(producer_client, new_sensor_pair, number_of_msg_to_send, producer_device_delay)
        update_monitor()

        # time.sleep(180) #wait 3 minutes(180 seconds) in between batches

    time.sleep(540) #wait 9 minutes(540 seconds) in between batches

    #Step 2_B Stop 30 producers every 5 minutes
    for x in range(0, 6):
        stop_N_Producer_Containers(producer_client, Monitor_list,30*scaling_factor)
        time.sleep(300)






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
experiment_run_time_seconds = 60
time.sleep(experiment_run_time_seconds)
print 'End Experiment'



print 'Stopping Monitors'
KafkaMonitor.stopMonitor()
ProducerMonitor.stopMonitor()
Spark_Cassandra_Monitor.stopMonitor()
PiMonitor.stopMonitor()


#wait for all threads to finish before ending the program
kafka_thread.join()
producerThread.join()
Spark_Cassandra_Thread.join()
Pi_thread.join()

time.sleep(10)




#kill the receivers after the experiment
#stopAndRemoveContainers(receiver_client)
iot_lb_1.remove_all_gateways()

time.sleep(10)






print '-----------------------------Done'

sys.exit(0)