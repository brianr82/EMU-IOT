import json
from collections import namedtuple
import time
from csv import DictWriter


class IoTMonitor:
    def __init__(self, dockerClientToMonitor):

        self.dockerClientToMonitor = dockerClientToMonitor
        self.previousRX = 0
        self.previousTX = 0
        self.previousCPU = 0.0
        self.previousSystem = 0.0
        self.exitFlag = True
        self.resultFileName = ''
        self.ActiveProducers = 0
        self.fileHeaderWritten = False
        self.hostCPUUsage = 0

    def calculateCPUPercentUnix(self, jsondata):
        cpuPercent = 0.0
        # calculate the change for the cpu usage of the container in between readings
        #cpu_delta = float(jsondata['cpu_stats']['cpu_usage']['total_usage']) - float(self.previousCPU)
        cpu_delta = float(jsondata['cpu_stats']['cpu_usage']['total_usage']) - float(jsondata['precpu_stats']['cpu_usage']['total_usage'])
        # calculate the change for the entire system between readings
        #systemDelta = float(jsondata['cpu_stats']['system_cpu_usage']) - float(self.previousSystem)
        systemDelta = float(jsondata['cpu_stats']['system_cpu_usage']) - float(jsondata['precpu_stats']['system_cpu_usage'])

        if systemDelta > 0.0 and cpu_delta > 0.0:
            cpuPercent = (cpu_delta / systemDelta) * 4 * 100.0

        return round(cpuPercent, 2)

    def calculateThroughput(self, jsondata):
        throughput = 0.0
        rx_delta = 0.0
        tx_delta = 0.0

        # calculate the change for the cpu usage of the container in between readings
        if (jsondata['networks']['eth0']['rx_bytes']) - (self.previousRX) > 0:
            rx_delta = float((jsondata['networks']['eth0']['rx_bytes']) - (self.previousRX)) / 1000
            # print rx_delta
        if (jsondata['networks']['eth0']['tx_bytes']) - (self.previousTX) > 0:
            tx_delta = float((jsondata['networks']['eth0']['tx_bytes']) - (self.previousTX)) / 1000
            # print tx_delta
        return {'tx_delta': tx_delta, 'rx_delta': rx_delta}

    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    '''
    *********************************************************************************************************
    '''

    def getUpdatedStats(self):

        aggregate_cpu = 0
        while self.exitFlag:
            time.sleep(5)
            all_containers = self.dockerClientToMonitor.containers.list(all)
            for container in all_containers:
                y = container.stats(decode=True, stream=False)
                # print y
                r = json.dumps(y)
                b = json.loads(r)
                # b = json.loads(y, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                # print b

                if self.previousCPU == 0.0:
                    # self.previousCPU = b.precpu_stats.cpu_usage.total_usage
                    self.previousCPU = b['precpu_stats']['cpu_usage']['total_usage']
                else:
                    print ('----------------------------------------------------')
                    print ('ResultFileName\t' + self.resultFileName)
                    print ('Container count\t' + str(len(self.dockerClientToMonitor.containers.list(all))))
                    # print 'Read Timestamp\t' + b.read
                    print ('Read Timestamp\t' + b['read'])
                    print ('Active Producers\t' + str(self.ActiveProducers))
                    # print 'MEM USAGE / LIMIT\t' + str(self.sizeof_fmt(b.memory_stats.usage)) + ' ' + str(self.sizeof_fmt(b.memory_stats.limit))


                    print ('MEM USAGE / LIMIT\t' + str(self.sizeof_fmt(b['memory_stats']['usage'])) + ' ' + str(
                        self.sizeof_fmt(b['memory_stats']['limit'])))
                    print ('MEM %\t' + str(
                        round(float(b['memory_stats']['usage']) / float(b['memory_stats']['limit']) * 100, 2)))
                    

                    #self.previousCPU = b['precpu_stats']['cpu_usage']['total_usage']
                    #self.previousSystem = b['precpu_stats']['system_cpu_usage']

                    container_cpu = self.calculateCPUPercentUnix (b)
                    print ('CPU %\t' + str(container_cpu))

                    aggregate_cpu = aggregate_cpu +container_cpu

                    throughput = self.calculateThroughput(b)
                    print ('Sent (kb/sec)\t' + str(throughput['tx_delta']))
                    print ('Received (kb/sec)\t' + str(throughput['rx_delta']))

                    self.previousRX = b['networks']['eth0']['rx_bytes']
                    self.previousTX = b['networks']['eth0']['tx_bytes']

                    # Write Data to File
                    record = [{
                        'sensor_count': str(self.ActiveProducers),
                        'name': container.name,
                        'timestamp': b['read'],
                        'cpu%': str(self.calculateCPUPercentUnix(b)),
                        'memory%': str(
                            round(float(b['memory_stats']['usage']) / float(b['memory_stats']['limit']) * 100, 2)),
                        'net_receive': str(throughput['rx_delta']),
                        'net_send': str(throughput['tx_delta']),
                        'memory_rss%': str(
                            round(float(b['memory_stats']['stats']['rss']) / float(b['memory_stats']['limit']) * 100, 2)),
                        'memory_active_anon%': str(
                            round(float(b['memory_stats']['stats']['active_anon']) / float(b['memory_stats']['limit']) * 100,
                                  2)),
                        }]

                    #self.append_experiment_reading_record(record)

                    keys = record[0].keys()
                    with open(self.get_result_file_name(), "a") as f:
                        dict_writer = DictWriter(f, keys, delimiter="\t")
                        if not self.fileHeaderWritten:
                            dict_writer.writeheader()
                            self.fileHeaderWritten = True
                        for value in record:
                            dict_writer.writerow(value)

            #write host level stats
            self.hostCPUUsage = aggregate_cpu  # return the total cpu usage for this monitor ie, this host
        return




    def stopMonitor(self):
        self.exitFlag = False

    def append_experiment_reading_record(self, record):
        keys = record[0].keys()
        with open(self.get_result_file_name(), "a") as f:
            dict_writer = DictWriter(f, keys, delimiter="\t")
            #dict_writer.writeheader()
            for value in record:
                dict_writer.writerow(value)

    def create_new_result_file(self, filename):
        self.set_result_file_name(filename)
        with open(self.get_result_file_name(), "w") as f:
            f.write('----------------------------------------------------------------' + '\n')

    def set_result_file_name(self, filename):
        self.resultFileName = filename

    def get_result_file_name(self):
        return self.resultFileName

    def set_active_producer_count(self, count):
        self.ActiveProducers = count

    def decrement_active_producer_count(self):
        self.ActiveProducers = self.ActiveProducers - 1




