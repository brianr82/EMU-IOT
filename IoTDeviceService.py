from abc import ABCMeta, abstractmethod


class IoTDeviceService(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.IoTDeviceList = []
        self.IoTDeviceCounter = 1

    @abstractmethod
    def addVirutalIoTDevice(self, IoTLoadBalancer, MonitorManager):
        pass


    def removeVirtualIoTDevice(self, IoTLoadBalancer, MonitorManager):
        if len(self.IoTDeviceList)== 0:
            print ('No more devices to remove!')
            return False
        else:

            # update all local lists
            removed_Iot_device = self.IoTDeviceList.pop ()
            self.decrementDeviceCounter ()

            # destroy the container
            removed_Iot_device.removeVirtualIoTSensor ()

            # remove the iot device from the Producer host and the virtual gateway
            removed_Iot_device.IoTProducerBinding.removeVirtualIoTDevice (removed_Iot_device)

            # update the monitor
            MonitorManager.updateActiveProducerCount (IoTLoadBalancer)
            return True


    def incrementDeviceCounter(self):
        self.IoTDeviceCounter = self.IoTDeviceCounter + 1

    def decrementDeviceCounter(self):
        self.IoTDeviceCounter = self.IoTDeviceCounter - 1