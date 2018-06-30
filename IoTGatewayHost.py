from IoTNode import *


class IoTGatewayHost(IoTNode):
    def __init__(self, NodeType,NodeName,NodeDockerRemoteClient,NodeIPAddress,NodeDockerPort,*boundNode):
        IoTNode.__init__ (self, NodeType, NodeName, NodeDockerRemoteClient, NodeIPAddress, NodeDockerPort, *boundNode)
        self.maxNumberOfVirtualIoTGatewaysSupported = 0
        self.virtualIoTGatewayList = []

    def addVirtualGateway(self,new_virtual_iotgateway):
        self.virtualIoTGatewayList.append(new_virtual_iotgateway)

    def removeVirtualGateway(self,virtual_IoTGateway):
        self.virtualIoTGatewayList.remove(virtual_IoTGateway)

    def hasFreeVirtualGateway(self,DeviceType):

        for virtual_gateway in self.virtualIoTGatewayList:
            if virtual_gateway.DeviceType == DeviceType and virtual_gateway.checkIfRoomtoAddDevice():
                return True
        else:
            print ('Could not find gateway type for this IoTDevice')
            return False


    def getNextFreeVirtualGateway(self,DeviceType):
        #check to see if this IotGatewayHost has room for at least one device
        if self.hasFreeVirtualGateway(DeviceType):
            #1. traverse virtualIoTGatewayList []
            for virtual_gateway in self.virtualIoTGatewayList:
                if virtual_gateway.DeviceType == DeviceType and virtual_gateway.checkIfRoomtoAddDevice():
                    usable_gateway = virtual_gateway
                    return usable_gateway
