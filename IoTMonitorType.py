from enum import Enum

class IoTMonitorType(Enum):

    kafka = 'KAFKA'  # type: IoTMonitorType
    spark = 'SPARK'
    cassandra = 'CASSANDRA'