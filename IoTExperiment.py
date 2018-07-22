
from abc import ABCMeta, abstractmethod
from IoTMonitorType import *

class IoTExperiment(object):
    __metaclass__ = ABCMeta
    def __init__(self):

        self.ExperimentName = None
        self.ApplicationToMonitor = None
        self.targetUtilization = None

    def setExperimentName(self,ExerimentName):
        self.ExperimentName = ExerimentName

    def setApplicationToMonitor(self,ApplicationToMonitor):
        assert isinstance(ApplicationToMonitor,IoTMonitorType)
        self.ApplicationToMonitor = ApplicationToMonitor

    def setTargetUtilization(self,TargetUtilization):
        self.TargetUtilization = TargetUtilization

    @abstractmethod
    def run(self):
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

