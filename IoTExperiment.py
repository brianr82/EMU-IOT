
from abc import ABCMeta, abstractmethod
from IoTMonitorType import *

class IoTExperiment(object):
    __metaclass__ = ABCMeta
    def __init__(self):

        self.ExperimentName = None
        self.ApplicationToMonitor = None
        self.targetCPUUtilization = None
        self.max_devices_on_a_producer_host = None
        self.max_devices_assigned_to_a_virtual_gateway = None

    def setExperimentName(self,ExerimentName):
        self.ExperimentName = ExerimentName

    def setApplicationToMonitor(self,ApplicationToMonitor):
        assert isinstance(ApplicationToMonitor,IoTMonitorType)
        self.ApplicationToMonitor = ApplicationToMonitor

    def setTargetCPUUtilization(self,targetCPUUtilization):
        self.targetCPUUtilization = targetCPUUtilization

    def set_max_devices_on_a_producer_host(self, max_devices_on_a_producer_host):
        self.max_devices_on_a_producer_host = max_devices_on_a_producer_host

    def set_max_devices_assigned_to_a_virtual_gateway(self, max_devices_assigned_to_a_virtual_gateway):
        self.max_devices_assigned_to_a_virtual_gateway = max_devices_assigned_to_a_virtual_gateway

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def configureExperiment(self, experiment_type):
        pass

    @abstractmethod
    def __IoTNodeSetup(self):
        pass

    @abstractmethod
    def __configureNetwork(self):
        pass

    @abstractmethod
    def __configureMonitor(self):
        pass

    @abstractmethod
    def __cleanUp(self):
        pass

    @abstractmethod
    def __executeWorkload(self):
        pass

    @abstractmethod
    def __generateTestCase(self):
        pass

