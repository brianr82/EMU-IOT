from IoTDevice import *
from IoTProducerHost import *
from IoTDeviceType import *



class IoTTemperatureSensor(IoTDevice):
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding,BoundIoTVirtualGateway,number_of_msg_to_send,producer_device_delay):
        IoTDevice.__init__ (self,IoTDeviceID,IoTDeviceName,IoTProducerBinding,BoundIoTVirtualGateway)
        #get the ip address of the gateway that is bound to the producer host
        self.destination_gateway_ip = self.IoTProducerBinding.boundNode.NodeIPAddress
        #get the port number for the  a virtual gateway
        self.destination_virtual_gateway_port = self.IoTProducerBinding.boundNode.getNextFreeVirtualGateway(IoTDeviceType.temperature).gateway_app_port
        self.number_of_msg_to_send = number_of_msg_to_send
        self.producer_device_delay = producer_device_delay
        self.BoundIoTVirtualGateway = BoundIoTVirtualGateway


    def createVirtualIoTSensor(self):
        self.IoTProducerBinding.NodeDockerRemoteClient.containers.run("brianr82/sensorsim:latest", \
                                           detach=True, \
                                           environment={'PI_IP': self.destination_gateway_ip, \
                                                        'PI_PORT': self.destination_virtual_gateway_port, \
                                                        'NUM_MSG': self.number_of_msg_to_send, \
                                                        'SENSOR_ID': self.IoTDeviceName, \
                                                        'DELAY': self.producer_device_delay}, \
                                           name=self.IoTDeviceName \
                                           )
        new_container = self.IoTProducerBinding.NodeDockerRemoteClient.containers.get(self.IoTDeviceName)
        print ('Created Container:\t' + new_container.name)


    def removeVirtualIoTSensor(self):

        existing_container = self.IoTProducerBinding.NodeDockerRemoteClient.containers.get(self.IoTDeviceName)
        existing_container.kill()
        existing_container.remove()
        print ('Removed Container:\t' + existing_container.name)