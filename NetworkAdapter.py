from iotticket.client import Client
from iotticket.models import datanodesvalue
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
from time import time
import json
class network_adapter:

    username = "LassiPee" #iot-ticket tili
    password = "Lorawandemo1234" #iot-ticket tilin
    baseurl = "https://my.iot-ticket.com/api/v1/"
    deviceId = "testi"

    def __init__(self):
        self.c = Client(self.baseurl, self.username, self.password)
        print ("network adapter initialized: " + str(self.c))
        self.dev= self.create_device()


    def findMyDevice(c):

        devices = c.getdevices()

        for dev in devices.deviceslist:
            if dev.name == c.deviceId:
                print("-------------------------------------------------------\n")
                print("Device {} found on server.".format(dev.name))
                print("-------------------------------------------------------\n")
                return dev

        return None

    def create_device(self):

        d = device()
        d.set_name("Lorawan end node")
        d.set_manufacturer("Wapice")
        d.set_type("employee")
        d.set_description("Im trainee")
        d.set_attributes(deviceattribute("packet", "counter"))

        c = Client(self.baseurl, self.username, self.password)

        c.registerdevice(d)


    def write_to_iot(self,data):

        # pack data to node object
        timeStamp = time()
        nv = datanodesvalue()
        nv.set_name("Lorawan")
        nv.set_path=("fingerno1")
        nv.set_dataType("double")
        packetcounter = float(data["seqno"])
        print(packetcounter)
        nv.set_value(packetcounter)
        nv.set_timestamp(timeStamp)

        rssi = data["gws"][0]
        float_rssi = float(rssi["rssi"])
        print("rssi: ", float_rssi)
        nv2 = datanodesvalue()
        nv2.set_name("Lorawan")
        nv2.set_path("fingerno2")
        nv2.set_dataType("double")
        nv2.set_value(float_rssi)
        nv2.set_timestamp(timeStamp)
        # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
        #nv1.set_timestamp(timeStamp)

        snr = data["gws"][0]
        float_snr = float(rssi["snr"])
        print("snr: ", float_snr)
        nv3 = datanodesvalue()
        nv3.set_name("Lorawan")
        nv3.set_path("fingerno3")
        nv3.set_dataType("double")
        nv3.set_value(float_snr)
        nv3.set_timestamp(timeStamp)
        # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
        #nv1.set_timestamp(timeStamp)

        print("nv1: ",nv)
        print("nv2: ", nv2)
        print("nv3: ", nv3)

        c = Client(self.baseurl, self.username, self.password)

        c.writedata("572ceee45cfc4a6c95ef3e7c4948f0ae", nv, nv2 ,nv3)


    def findMyDevice(self):

        devices = self.c.getdevices()

        for dev in devices.deviceslist:
            if dev.name == self.c.deviceId:
                print("-------------------------------------------------------\n")
                print("Device {} found on server.".format(dev.name))
                print("-------------------------------------------------------\n")
                return dev

        return None

