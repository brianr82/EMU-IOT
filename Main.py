from IoTExperimentLinear import *
from IoTMonitorType import *

import sys


#Run these on the respective docker machines
# docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
# docker build --no-cache=true -f latest/Dockerfile https://github.com/brianr82/node-red-docker.git -t brianr82/multinodered:latest




IoTExperiment = IoTExperimentLinear()


IoTExperiment.setExperimentName("Refactor_1")
IoTExperiment.setApplicationToMonitor(IoTMonitorType.cassandra)
IoTExperiment.setTargetCPUUtilization(200)
IoTExperiment.set_max_devices_on_a_producer_host(200)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(50)
IoTExperiment.run()


print('-----------------------------Done')

sys.exit(0)