class receiver:
    def __init__(self, receiver_name,port_number):
        self.receiver = receiver_name
        self.port_number = port_number


    def get_receiver_name(self):
        return self.receiver

    def get_port_number(self):
        return self.port_number
