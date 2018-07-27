from IoTDeviceType import *
from IoTTemperatureSensor import IoTTemperatureSensor
from IoTCamera import *


class IoTDeviceServiceCamera():
    def __init__(self):
        self.IoTDeviceList = []
        self.IoTDeviceCounter = 1


    def addVirutalIoTDevice(self, IoTLoadBalancer, MonitorManager):

        destination_producer_host = IoTLoadBalancer.get_target_iot_device_edge ('create')
        IoTProducerBinding = destination_producer_host
        IoTDeviceID = 'test'

        # Temperature sensor implementation

        # virtual device options(i.e. the params passed to the docker container when its created)
        number_of_msg_to_send = 10000000
        producer_device_delay = 1000000

        BoundIoTVirtualGateway = destination_producer_host.boundNode.getNextFreeVirtualGateway (IoTDeviceType.camera)

        producer_prefix = 'IoT_camera_' + str (self.IoTDeviceCounter) + '_'

        IoTDeviceName = destination_producer_host.NodeName + '_' + producer_prefix + str (
            BoundIoTVirtualGateway.gateway_app_port)

        new_sensor = IoTCamera (IoTDeviceID, IoTDeviceName, IoTProducerBinding, BoundIoTVirtualGateway,number_of_msg_to_send, producer_device_delay)
        # add device to list
        self.IoTDeviceList.append (new_sensor)
        # Start the sensor

        new_sensor.createVirtualIoTSensor ()

        # add device to producer host
        IoTProducerBinding.addVirtualIoTDevice (new_sensor)



        # increment local device counter
        self.incrementDeviceCounter()
        # update the monitor
        MonitorManager.updateActiveProducerCount (IoTLoadBalancer)




    def removeVirtualIoTDevice(self, IoTLoadBalancer, MonitorManager):

        #update all local lists
        removed_Iot_device = self.IoTDeviceList.pop()
        self.decrementDeviceCounter()

        #destroy the container
        removed_Iot_device.removeVirtualIoTSensor()

        #find the Producer binding where this device is located
        removed_Iot_device.IoTProducerBinding.removeVirtualIoTDevice(removed_Iot_device)





    def incrementDeviceCounter(self, deviceType):
        self.IoTDeviceCounter = self.IoTDeviceCounter + 1

    def decrementDeviceCounter(self, deviceType):
        self.IoTDeviceCounter = self.IoTDeviceCounter - 1