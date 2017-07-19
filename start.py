import docker
import time
from dockerSensor import createReceiver
from dockerSensor import printContainers
from dockerSensor import stopContainers
from dockerSensor import createProducer



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
#receiver_manager_docker_ip = '192.168.2.138'
receiver_manager_docker_ip = '10.12.7.45'
receiver_manager_docker_port = '2375'


start_remote_port_range = 2000
number_of_sensor_receiver_pairs = 2
end_remote_port_range = start_remote_port_range + number_of_sensor_receiver_pairs

'''
Main Program
'''

#Create to producer and receiver client to create new virtual sensors
producer_client = docker.DockerClient(base_url='tcp://'+producer_manager_docker_ip+':'+producer_manager_docker_port)
receiver_client = docker.DockerClient(base_url='tcp://'+receiver_manager_docker_ip+':'+receiver_manager_docker_port)



createReceiver(receiver_client,2000)
time.sleep(20)

createProducer(producer_client,receiver_manager_docker_ip,2000,100,'0001')

printContainers(receiver_client)
printContainers(producer_client)

time.sleep(20)




stopContainers(receiver_client)
stopContainers(producer_client)


