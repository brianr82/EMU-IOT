class Sensorpair:
    def __init__(self, port_number, producer_name,receiver_name):
        self.receiver = receiver_name
        self.port_number = port_number
        self.producer = producer_name

    def get_receiver_name(self):
        return self.receiver

    def get_producer_name(self):
        return self.producer

    def get_port_number(self):
        return self.port_number




