from enum import Enum

class IoTMonitorType(Enum):

    kafka = 'KAFKA'  # type: IoTMonitorType
    spark = 'SPARK' # type: IoTMonitorType
    cassandra = 'CASSANDRA' # type: IoTMonitorType