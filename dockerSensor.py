
import time


def createSensorPair(receiver_client,producer_client,receiver_manager_docker_ip, port_num, NUM_MSG, SENSOR_ID):

    createReceiver(receiver_client,port_num)
    time.sleep(5)
    createProducer(producer_client, receiver_manager_docker_ip, port_num, NUM_MSG,SENSOR_ID)


def createReceiver(receiver_client,port_num):

    receiver_client.containers.run("brianr82/multinodered:latest", \
                                   detach=True,\
                                   ports={'1880/tcp': port_num}, \
                                   environment={'FLOWS': 'sensor_flows.json'}, \
                                   name='receiver_' + str(port_num) \
                                   )
    new_container = receiver_client.containers.get('receiver_' + str(port_num))
    print 'Created Container\t' + new_container.name


def createProducer(producer_client,PI_IP,PI_PORT,NUM_MSG,SENSOR_ID):

    producer_client.containers.run("brianr82/sensorsim:latest", \
                                   detach=True,\
                                   environment={'PI_IP': PI_IP, \
                                   'PI_PORT': PI_PORT,\
                                   'NUM_MSG': NUM_MSG, \
                                   'SENSOR_ID':'simsensor' + str(SENSOR_ID)}, \
                                   name='sensor_' + str(PI_PORT) \
                                   )
    new_container = producer_client.containers.get('sensor_' + str(PI_PORT))
    print 'Created Container\t' + new_container.name


def printContainers(client_manager):
    # print list of created containers
    for container in client_manager.containers.list(all):
        print 'Created container\t' + container.name


def stopContainers(client_manager):

    # stop created containers
    for container in client_manager.containers.list(all):
        print 'Stopping container\t' + container.name
        container.stop()
        container.remove()