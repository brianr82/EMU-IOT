from IoTExperimentLinear import *


import sys


#Run these on the respective docker machines
# docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
# docker build --no-cache=true -f latest/Dockerfile https://github.com/brianr82/node-red-docker.git -t brianr82/multinodered:latest

search_method = 'Linear_'
experiment_type = 'camera'

experiment_number = 3
target_cpu_utilization = 120
max_devices_on_a_producer_host = 100
max_devices_assigned_to_a_virtual_gateway = 25


IoTExperiment = IoTExperimentLinear()



experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()


time.sleep(60)


experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)




experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)


experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)


experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()


time.sleep(60)


experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)




experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)

'''


experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)




experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)




experiment_number +=1
IoTExperiment.setExperimentName(search_method+experiment_type+str(experiment_number))
IoTExperiment.configureExperiment(experiment_type)
IoTExperiment.setTargetCPUUtilization(target_cpu_utilization)
IoTExperiment.set_max_devices_on_a_producer_host(max_devices_on_a_producer_host)
IoTExperiment.set_max_devices_assigned_to_a_virtual_gateway(max_devices_assigned_to_a_virtual_gateway)
IoTExperiment.run()



time.sleep(60)

'''



print('-----------------------------Done')

sys.exit(0)