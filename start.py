import docker
import time

'''
An application that will start synthetic sensors, and the corresponding receivers on the PI
'''


'''
Configs
'''

#configs for docker machine that will host the synthetic sensors
producer_manager_docker_ip = '192.168.2.138'
producer_manager_docker_port = '2375'

#configs for docker machine that will host the receiver gateway(Pi) that has a connection to kafka
receiver_manager_docker_ip = '192.168.2.138'
receiver_manager_docker_port = '2375'


start_remote_port_range = 2000
number_of_sensor_receiver_pairs = 50

end_remote_port_range = start_remote_port_range + number_of_sensor_receiver_pairs

'''
Main Program
'''

#Create to producer and receiver client to create new virtual sensors
producer_client = docker.DockerClient(base_url='tcp://'+producer_manager_docker_ip+':'+producer_manager_docker_port)
receiver_client = docker.DockerClient(base_url='tcp://'+receiver_manager_docker_ip+':'+receiver_manager_docker_port)


#first remove all exited containers


#create new receiver client, verify its online then create a producer client, and verify that its online

for port_num in range(start_remote_port_range,end_remote_port_range):
    receiver_client.containers.run("brianr82/multinodered:latest",\
                                   detach=True, ports= {'1880/tcp': port_num},\
                                   environment={'FLOWS': 'sensor_flows.json'},\
                                   name = 'recevier_'+ str(port_num)\
                                   )


#for image in producer_client.images.list():
#    print (image.id + '\n')
for container in receiver_client.containers.list(all):
    print 'Created container\t' + container.name

time.sleep(5)
for container in receiver_client.containers.list(all):
    print 'Stopping container\t' + container.name
    container.stop()
    container.remove()




#Create to receiver client to create new receiver gateway










#function create producer sensor

#function create receiver  http endpoint


