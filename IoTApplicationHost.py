from IoTNode import *

class IoTApplicationHost(IoTNode):
    def __init__(self, NodeType, NodeName, NodeDockerRemoteClient, NodeIPAddress, NodeDockerPort, *boundNode):
        IoTNode.__init__ (self, NodeType, NodeName, NodeDockerRemoteClient, NodeIPAddress, NodeDockerPort, *boundNode)