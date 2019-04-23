from IoTDeviceType import *
from IoTCamera import *
from IoTDeviceService import *
import logging


class IoTDeviceServiceCamera(IoTDeviceService):
    def __init__(self):
        IoTDeviceService.__init__(self)


    def addVirutalIoTDevice(self, IoTLoadBalancer, MonitorManager):

        destination_producer_host = IoTLoadBalancer.get_free_IoTProducerHost ()
        IoTProducerBinding = destination_producer_host
        IoTDeviceID = 'test'

        # Temperature sensor implementation

        # virtual device options(i.e. the params passed to the docker container when its created)
        image_quality = 5
        producer_device_delay = 1
        destination_sink_ip = '10.12.7.64'


        BoundIoTVirtualGateway = destination_producer_host.boundNode.getNextFreeVirtualGateway (IoTDeviceType.camera)

        producer_prefix = 'IoT_camera_' + str (self.IoTDeviceCounter) + '_'

        IoTDeviceName = destination_producer_host.NodeName + '_' + producer_prefix + str(BoundIoTVirtualGateway.gateway_app_port)

        new_sensor = IoTCamera (IoTDeviceID, IoTDeviceName, IoTProducerBinding, BoundIoTVirtualGateway, destination_sink_ip, image_quality, producer_device_delay)
        # add device to list
        self.IoTDeviceList.append (new_sensor)
        # Start the sensor

        new_sensor.createVirtualIoTSensor()

        # add device to producer host
        IoTProducerBinding.addVirtualIoTDevice (new_sensor)



        # increment local device counter
        self.incrementDeviceCounter()
        # update the monitor
        MonitorManager.updateActiveProducerCount (IoTLoadBalancer)