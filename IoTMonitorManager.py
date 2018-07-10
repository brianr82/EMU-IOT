from  IoTMonitorType import *

class IoTMonitorManager():
    def __init__(self):
        self.IoTMonitorList = []
        self.IoTMonitorThreadList = []

    def addMonitor(self,IoTMonitorToAdd):
        self.IoTMonitorList.append(IoTMonitorToAdd)

    def getMonitor(self):


        return


    def addThread(self, ThreadToAdd):
        self.IoTMonitorThreadList.append (ThreadToAdd)

    def updateActiveProducerCount(self,IoTLoadBalancer):
        for monitor in self.IoTMonitorList:
            monitor.set_active_producer_count (IoTLoadBalancer.get_current_iot_device_count())

    def stopAllMonitors(self):
        for monitor in self.IoTMonitorList:
            monitor.stopMonitor()

    def startAllMonitors(self):
        for thread in self.IoTMonitorThreadList:
            thread.start()

    def joinThreads(self):
        for thread in self.IoTMonitorThreadList:
            thread.join()
