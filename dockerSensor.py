
import time


def createSensorPair(receiver_client,producer_client,receiver_manager_docker_ip, port_num, NUM_MSG,DELAY_SECONDS,KafkaMonitor,ProducerMonitor,Spark_Cassandra_Monitor,PiMonitor):

    createReceiver(receiver_client,port_num)
    time.sleep(10)  #wait 10 seconds to let receiver initialize
    for x in range(1,5): #create 20 producers
        #update the active producer counts in each monitor
        createProducer(producer_client, receiver_manager_docker_ip, port_num, NUM_MSG, str(x), DELAY_SECONDS)

        KafkaMonitor.set_active_producer_count(len(producer_client.containers.list(all)))
        ProducerMonitor.set_active_producer_count(len(producer_client.containers.list(all)))
        Spark_Cassandra_Monitor.set_active_producer_count(len(producer_client.containers.list(all)))
        PiMonitor.set_active_producer_count(len(producer_client.containers.list(all)))



        time.sleep(10) # add a new producer every 10 seconds






def createReceiver(receiver_client,port_num):

    receiver_client.containers.run("brianr82/multinodered:latest", \
                                   detach=True,\
                                   ports={'1880/tcp': port_num}, \
                                   environment={'FLOWS': 'sensor_flows.json'}, \
                                   name='receiver_' + str(port_num) \
                                   )
    new_container = receiver_client.containers.get('receiver_' + str(port_num))
    print 'Created Container\t' + new_container.name


def createProducer(producer_client,PI_IP,PI_PORT,NUM_MSG,SENSOR_ID,DELAY_SECONDS):

    producer_client.containers.run("brianr82/sensorsim:latest", \
                                   detach=True,\
                                   environment={'PI_IP': PI_IP, \
                                   'PI_PORT': PI_PORT,\
                                   'NUM_MSG': NUM_MSG, \
                                   'SENSOR_ID':'simsensor_' + str(PI_PORT) +"_"+ SENSOR_ID, \
                                   'DELAY': DELAY_SECONDS}, \
            name='sensor_' + str(PI_PORT) +"_"+ SENSOR_ID \
                                   )
    new_container = producer_client.containers.get('sensor_' + str(PI_PORT) +"_"+ SENSOR_ID)
    print 'Created Container\t' + new_container.name




def createReceiverNew(receiver_client,receiver):

    receiver_client.containers.run("brianr82/multinodered:latest", \
                                   detach=True,\
                                   ports={'1880/tcp': receiver.get_port_number()}, \
                                   environment={'FLOWS': 'sensor_flows.json'}, \
                                   name=receiver.get_receiver_name() \
                                  )
    new_container = receiver_client.containers.get(receiver.get_receiver_name())
    print 'Created Container\t' + new_container.name


def createProducerNew(producer_client,sensor_pair,NUM_MSG,DELAY_SECONDS):

    producer_client.containers.run("brianr82/sensorsim:latest", \
                                   detach=True,\
                                   environment={'PI_IP': sensor_pair.get_receiver_ip(), \
                                   'PI_PORT': sensor_pair.get_port_number(),\
                                   'NUM_MSG': NUM_MSG, \
                                   'SENSOR_ID':sensor_pair.get_producer_name(), \
                                   'DELAY': DELAY_SECONDS}, \
                                    name=sensor_pair.get_producer_name() \
                                   )
    new_container = producer_client.containers.get(sensor_pair.get_producer_name())
    print 'Created Container\t' + new_container.name














def printContainers(client_manager):
    # print list of created containers
    for container in client_manager.containers.list(all):
        print 'Created container\t' + container.name


def stopAllProducerContainers(client_manager,client_monitor_list):

    # stop created containers
    for container in client_manager.containers.list(all):
        print 'Stopping container\t' + container.name
        container.stop()
        container.remove()
        for monitor in client_monitor_list:
            monitor.decrement_active_producer_count()


def stop_N_Producer_Containers(client_manager,client_monitor_list,number_producers_to_stop):

    # get the list of all containers
    container_list = client_manager.containers.list(all)

    #check to make sure  you arent trying to destroy more producers than what's active
    if number_producers_to_stop > len(container_list):
        number_producers_to_stop = len(container_list)

    #stop the desired amount of containers
    for x in range(0,number_producers_to_stop):
        container = container_list[x]
        print 'Stopping container\t' + container.name
        container.kill()
        container.remove()
        for monitor in client_monitor_list:
            monitor.decrement_active_producer_count()


def stopContainers(client_manager):

    # stop created containers
    for container in client_manager.containers.list(all):
        print 'Stopping container\t' + container.name
        container.stop()
        container.remove()
