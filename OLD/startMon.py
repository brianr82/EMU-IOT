import docker
from IoTMonitor import monitor2
from threading import Thread
from threading import Thread
import json
import time

import docker

#configs for docker machine that will host the synthetic sensors
producer_manager_docker_ip = '10.12.7.42'
producer_manager_docker_port = '2375'

#configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
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







'''
exitflag = True

def A(dockerClient):
    all_containers = dockerClient.containers.list(all)
    while exitflag:
        for container in all_containers:
         #for y in container.stats(stream=False):
            y = container.stats(decode=True,stream =False)
              #print y
            r = json.dumps(y)
            b =  json.loads(r)
                            #b = json.loads(y, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            print b['name']

t1 = Thread(target=A,args=(kafka_client,))
t2 = Thread(target=A,args=(receiver_client,))
t1.start()
t2.start()


time.sleep(10)
exitflag = False

'''


KafkaMonitor = monitor2(kafka_client)
kafka_thread = Thread(target=KafkaMonitor.createNewMonitor)
kafka_thread.start()

ProducerMonitor = monitor2(producer_client)
producerThread = Thread(target=ProducerMonitor.createNewMonitor)
producerThread.start()


print 'Monitor Started'
time.sleep(20)

print 'Stopping Monitors'
KafkaMonitor.stopMonitor()
ProducerMonitor.stopMonitor()


