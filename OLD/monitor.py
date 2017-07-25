import docker
import json
import os
from collections import namedtuple
from csv import DictWriter




def getDockerStats(dockerClientToMonitor):

    containers = dockerClientToMonitor.containers.list(all)

    for c in containers:
        container = dockerClientToMonitor.containers.get(c.name)
        for x in container.stats(stream= 'true'):
            b = json.loads(x, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            #print x
            print '----------------------------------------------------'
            print 'Container count\t' + str(len(dockerClientToMonitor.containers.list(all)))
            print 'Read Timestamp\t' + b.read
            print 'CPU Usage\t' + str(b.cpu_stats.cpu_usage.total_usage)
            print 'Memory Usage\t' + str(b.memory_stats.usage)
            print 'Network Tx\t' + str(b.networks.eth0.rx_bytes)
            print 'Network Rx\t' + str(b.networks.eth0.tx_bytes)

            return [{
                'name': container.name,
                'timestamp': b.read,\
                'cpu': str(b.cpu_stats.cpu_usage.total_usage),\
                'memory':  str(b.memory_stats.usage), \
                'network_rx': str(b.networks.eth0.rx_bytes), \
                'network_tx': str(b.networks.eth0.tx_bytes), \
            }]



def append_record(record,filename):
#    with open('experimentstats', 'a') as f:
#        json.dump(record, f)
        #f.write(os.linesep)
    keys = record[0].keys()
    with open(filename, "a") as f:
        dict_writer = DictWriter(f, keys, delimiter="\t")
        #dict_writer.writeheader()
        for value in record:
            dict_writer.writerow(value)



