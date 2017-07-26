import docker
import time
import datetime
from monitor2 import *
from threading import Thread
from dockerSensor import stopContainers
from dockerSensor import createSensorPair
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
receiver_manager_docker_ip = '10.7.7.14'
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

experiment_tag = 'Run1'
directory = 'ExperimentResults/'

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
Experiment Settings
'''


'''
add 10 sensors
'''
def workloadA():
    start_remote_port_range = 2000
    number_of_sensor_receiver_pairs = 4
    end_remote_port_range = start_remote_port_range + number_of_sensor_receiver_pairs

    number_of_msg_to_send = 10000
    producer_device_delay = 500000

    for port_num in range(start_remote_port_range, end_remote_port_range):
        createSensorPair(receiver_client,producer_client,receiver_manager_docker_ip,port_num,number_of_msg_to_send,producer_device_delay,KafkaMonitor,ProducerMonitor,Spark_Cassandra_Monitor)






print 'Starting Experiment'

workloadA()
#workloadB()


experiment_run_time_seconds = 600
time.sleep(experiment_run_time_seconds)
print 'End Experiment'

'''
*****************************************************************************************************
Clean up
*****************************************************************************************************
'''

print 'Stopping Monitors'
KafkaMonitor.stopMonitor()
ProducerMonitor.stopMonitor()
Spark_Cassandra_Monitor.stopMonitor()


#wait for all threads to finish before ending the program
kafka_thread.join()
producerThread.join()
Spark_Cassandra_Thread.join()

time.sleep(10)
print 'Stopping Producers and Receivers'
stopContainers(receiver_client)
stopContainers(producer_client)






print '-----------------------------Done'

sys.exit(0)