import docker
import time
from monitor import getDockerStats,append_record

from dockerSensor import printContainers
from dockerSensor import stopContainers
from dockerSensor import createSensorPair

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
#receiver_manager_docker_ip = '192.168.2.138'
receiver_manager_docker_ip = '10.12.7.45'
receiver_manager_docker_port = '2375'



kafka_manager_docker_ip = '10.12.7.35'
kafka_manager_docker_port = '2375'










start_remote_port_range = 2000
number_of_sensor_receiver_pairs = 2
end_remote_port_range = start_remote_port_range + number_of_sensor_receiver_pairs

'''
Main Program
'''

#Create to producer and receiver client to create new virtual sensors
producer_client = docker.DockerClient(base_url='tcp://'+producer_manager_docker_ip+':'+producer_manager_docker_port)
receiver_client = docker.DockerClient(base_url='tcp://'+receiver_manager_docker_ip+':'+receiver_manager_docker_port)
kafka_client = docker.DockerClient(base_url='tcp://'+kafka_manager_docker_ip+':'+kafka_manager_docker_port)




i = 0
for port_num in range(start_remote_port_range, end_remote_port_range):
    createSensorPair(receiver_client,producer_client,receiver_manager_docker_ip,port_num,1000,i,2)
    i=i+1
    record = getDockerStats(kafka_client)
    append_record(record,'experimentstats1')




print 'Starting Experiment'
time.sleep(60)
print 'End Experiment'


stopContainers(receiver_client)
stopContainers(producer_client)



print '-----------------------------Done'


