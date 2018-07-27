from IoTDeviceType import *
from IoTTemperatureSensor import IoTTemperatureSensor
from IoTDeviceService import *


class IoTDeviceServiceTemperature(IoTDeviceService):
    def __init__(self):
        IoTDeviceService.__init__(self)

    def addVirutalIoTDevice(self, IoTLoadBalancer, MonitorManager):

        destination_producer_host = IoTLoadBalancer.get_free_IoTProducerHost()
        IoTProducerBinding = destination_producer_host
        IoTDeviceID = 'test'

        # Temperature sensor implementation

        # virtual device options(i.e. the params passed to the docker container when its created)
        number_of_msg_to_send = 10000000
        producer_device_delay = 1000000


        BoundIoTVirtualGateway = destination_producer_host.boundNode.getNextFreeVirtualGateway(IoTDeviceType.temperature)

        producer_prefix = 'IoT_temperature_sensor_' + str(self.IoTDeviceCounter) + '_'

        IoTDeviceName = destination_producer_host.NodeName + '_' + producer_prefix + str(BoundIoTVirtualGateway.gateway_app_port)

        new_sensor = IoTTemperatureSensor(IoTDeviceID, IoTDeviceName, IoTProducerBinding, BoundIoTVirtualGateway,number_of_msg_to_send, producer_device_delay)
        # add device to list
        self.IoTDeviceList.append(new_sensor)
        # Start the sensor

        new_sensor.createVirtualIoTSensor()

        # add device to producer host
        IoTProducerBinding.addVirtualIoTDevice(new_sensor)



        # increment local device counter
        self.incrementDeviceCounter()
        # update the monitor
        MonitorManager.updateActiveProducerCount(IoTLoadBalancer)
