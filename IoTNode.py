class IoTNode:
    def __init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode):
        self.NodeType = NodeType
        self.NodeName = NodeName
        self.NodeDockerRemoteClient = NodeDockerRemoteClient
        self.NodeIPAddress = NodeIPAddress
        self.NodeDockerPort = NodeDockerPort
        self.boundNode = boundNode


    def bindToIoTNode(self,nodeToBind):
        self.boundNode = nodeToBind


