import time

def createAllReceivers(receiver_client,start_remote_port_range,end_remote_port_range):
    # create new receiver client, verify its online then create a producer client, and verify that its online
    for port_num in range(start_remote_port_range, end_remote_port_range):
        createReceiver(receiver_client,port_num)



def createReceiver(receiver_client,port_num):
    receiver_client.containers.run("brianr82/multinodered:latest", \
                                   detach=True,\
                                   ports={'1880/tcp': port_num}, \
                                   environment={'FLOWS': 'sensor_flows.json'}, \
                                   name='receiver_' + str(port_num) \
                                   )

def createProducer(producer_client,PI_IP,PI_PORT,NUM_MSG,SENSOR_ID):
    producer_client.containers.run("brianr82/sensorsim:latest", \
                                   detach=True,\
                                   environment={'PI_IP': PI_IP, \
                                   'PI_PORT': PI_PORT,\
                                   'NUM_MSG': NUM_MSG, \
                                   'SENSOR_ID':'sensor' + str(SENSOR_ID)}, \
                                   name='sensor_' + str(PI_PORT) \
                                   )


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