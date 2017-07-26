from SensorPair import *

sensor_pair_list = []

number_of_receivers = 5
number_of_sensors = 100
number_of_sensors_assigned_to_receiver = number_of_sensors / number_of_receivers

start_remote_port_range = 2000
end_remote_port_range = start_remote_port_range + number_of_receivers

receiver_prefix = 'receiver_'
producer_prefix = 'simsensor_'

receiver_list=[]
sensor_list=[]



for port_number in range(start_remote_port_range, end_remote_port_range):
    for suffix_id in range(1, number_of_sensors_assigned_to_receiver +1):
        receiver_name = receiver_prefix + str(port_number)
        producer_name = producer_prefix + str(port_number) +'_' + str(suffix_id)
        sensor_pair_list.append(Sensorpair(port_number, producer_name,receiver_name ))

for x in sensor_pair_list:
    print x.get_receiver_name() + '\t' + x.get_producer_name() + '\t' + str(x.get_port_number())

