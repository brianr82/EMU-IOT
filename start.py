import docker
import time
import datetime
from receiver import *
from monitor2 import *
from threading import Thread
from dockerSensor import *
from SensorPair import *



import sys

#Run these on the respective docker machines
# docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
# docker build --no-cache=true -f latest/Dockerfile https://github.com/brianr82/node-red-docker.git -t brianr82/multinodered:latest



'''
An application that will start synthetic sensors, and the corresponding receivers on the PI
'''


'''
Configs
'''

#configs for docker machine that will host the synthetic sensors
producer_manager_docker_ip = '10.12.7.42'
producer_manager_docker_port = '2375'
#configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
receiver_manager_docker_ip = '10.12.7.45'
receiver_manager_docker_port = '2375'
#configs for docker machine that will host the kafka cluster
kafka_manager_docker_ip = '10.12.7.35'
kafka_manager_docker_port = '2375'
#configs for docker machine that will host the spark_cassandra instances
spark_cassandra_manager_docker_ip = '10.12.7.41'
spark_cassandra_manager_docker_port = '2375'



#Create to producer and receiver client to create new virtual sensors
producer_client = docker.DockerClient(base_url='tcp://'+producer_manager_docker_ip+':'+producer_manager_docker_port)
receiver_client = docker.DockerClient(base_url='tcp://'+receiver_manager_docker_ip+':'+receiver_manager_docker_port)
kafka_client = docker.DockerClient(base_url='tcp://'+kafka_manager_docker_ip+':'+kafka_manager_docker_port)
spark_cassandra_client = docker.DockerClient(base_url='tcp://'+spark_cassandra_manager_docker_ip+':'+spark_cassandra_manager_docker_port)

'''
*****************************************************************************************************************
Experiment Monitors
*****************************************************************************************************************
'''

'''
Start the monitors
'''

experiment_tag = 'Run_1_second_vir'
directory = 'ExperimentResults/'


PiMonitor = monitor2(receiver_client)
PiMonitor.create_new_result_file(directory+'PiReadings_'+ experiment_tag)
Pi_thread = Thread(target=PiMonitor.createNewMonitor)

Pi_thread.start()


KafkaMonitor = monitor2(kafka_client)
KafkaMonitor.create_new_result_file(directory+'KafkaReadings_'+ experiment_tag)
kafka_thread = Thread(target=KafkaMonitor.createNewMonitor)

kafka_thread.start()


ProducerMonitor = monitor2(producer_client)
ProducerMonitor.create_new_result_file(directory+'Producer_Readings_'+experiment_tag)
producerThread = Thread(target=ProducerMonitor.createNewMonitor)

producerThread.start()


Spark_Cassandra_Monitor = monitor2(spark_cassandra_client)
Spark_Cassandra_Monitor.create_new_result_file(directory+'Spark_Cassandra_Readings_'+ experiment_tag)
Spark_Cassandra_Thread = Thread(target=Spark_Cassandra_Monitor.createNewMonitor)

Spark_Cassandra_Thread.start()



Monitor_list = []

Monitor_list.append(PiMonitor)
Monitor_list.append(KafkaMonitor)
Monitor_list.append(ProducerMonitor)
Monitor_list.append(Spark_Cassandra_Monitor)


def update_monitor():
    KafkaMonitor.set_active_producer_count(len(producer_client.containers.list(all)))
    ProducerMonitor.set_active_producer_count(len(producer_client.containers.list(all)))
    Spark_Cassandra_Monitor.set_active_producer_count(len(producer_client.containers.list(all)))
    PiMonitor.set_active_producer_count(len(producer_client.containers.list(all)))




print 'Monitors Started'
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
Workload B ************************************************************************************************************
'''

def workloadB():


    sensor_pair_list = []


    scaling_factor = 5
    number_of_receivers = 5 * scaling_factor
    number_of_sensors = 90 * scaling_factor
    number_of_sensors_assigned_to_receiver = number_of_sensors / number_of_receivers

    start_remote_port_range = 2000
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
            sensor_pair_list.append(Sensorpair(port_number, producer_name, receiver_name,receiver_manager_docker_ip))

    #create all the receivers
    for r in receiver_list:
        createReceiverNew(receiver_client,r)
        time.sleep(5)

    time.sleep(10)





    '''
    Define workload profile below
    '''
    #create the producers as needed

    number_of_msg_to_send = 10000
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


#workloadA()
workloadB()




'''
*****************************************************************************************************
Clean up
*****************************************************************************************************
'''
experiment_run_time_seconds = 60
time.sleep(experiment_run_time_seconds)
print 'End Experiment'


#kill the receivers after the experiment
stopContainers(receiver_client)


time.sleep(10)

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






print '-----------------------------Done'

sys.exit(0)