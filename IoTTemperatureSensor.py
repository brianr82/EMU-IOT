from IoTDevice import *



class IotTemperatureSensor(IoTDevice):

    #get the ip address of the gateway that is bound to the producer host
    destination_gateway_ip  = self.IoTProducerBinding.boundNode.NodeDockerRemoteClient

    def createIoTVirtualTemperatureSensor(self):
        self.TargetProducerHost.containers.run("brianr82/sensorsim:latest", \
                                           detach=True, \
                                           environment={'PI_IP': self.destination_gateway_ip, \
                                                        'PI_PORT': sensor_pair.get_port_number(), \
                                                        'NUM_MSG': NUM_MSG, \
                                                        'SENSOR_ID': self.IoTDeviceName, \
                                                        'DELAY': DELAY_SECONDS}, \
                                           name=sensor_pair.get_producer_name() \
                                           )
        new_container = self.TargetProducerHost.containers.get(sensor_pair.get_producer_name())
        print 'Created Container\t' + new_container.name