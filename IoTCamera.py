from IoTDevice import *
from IoTProducerHost import *
from IoTDeviceType import *

#"IoT_Camera_01" "10.12.7.5" "5" "1" --name emu01


class IoTCamera(IoTDevice):
    def __init__(self,IoTDeviceID,IoTDeviceName,IoTProducerBinding,BoundIoTVirtualGateway,cassandra_ip,image_quality,producer_device_delay):
        IoTDevice.__init__ (self,IoTDeviceID,IoTDeviceName,IoTProducerBinding,BoundIoTVirtualGateway)
        #get the ip address of the gateway that is bound to the producer host
        self.destination_gateway_ip = self.IoTProducerBinding.boundNode.NodeIPAddress
        #get the port number for the  a virtual gateway
        self.destination_virtual_gateway_port = self.IoTProducerBinding.boundNode.getNextFreeVirtualGateway(IoTDeviceType.camera).gateway_app_port
        self.cassandra_ip = cassandra_ip
        self.image_quality = image_quality
        self.producer_device_delay = producer_device_delay

    def createVirtualIoTSensor(self):
        self.IoTProducerBinding.NodeDockerRemoteClient.containers.run("brianr82/emulated-camera:latest", \
                                           detach=True, \
                                           environment={'SENSOR_ID': self.IoTDeviceName, \
                                                        'CASSANDRA_IP': self.cassandra_ip, \
                                                        'IMG_QUALITY': self.image_quality, \
                                                        'DELAY': self.producer_device_delay}, \
                                           name=self.IoTDeviceName \
                                           )
        new_container = self.IoTProducerBinding.NodeDockerRemoteClient.containers.get(self.IoTDeviceName)
        print ('Created Container\t' + new_container.name)

    def removeVirtualIoTSensor(self):

        existing_container = self.IoTProducerBinding.NodeDockerRemoteClient.containers.get(self.IoTDeviceName)
        existing_container.kill()
        existing_container.remove()
        print ('Removed Container:\t' + existing_container.name)