from iotticket.client import Client
from iotticket.models import datanodesvalue
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
from datetime import datetime
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
        Ts = datetime.now()
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
        nv2.set_name("RSSI")
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
        nv3.set_name("SNR")
        nv3.set_path("fingerno2")
        nv3.set_dataType("double")
        nv3.set_value(float_snr)
        nv3.set_timestamp(timeStamp)
        # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
        #nv1.set_timestamp(timeStamp)

        timetost = data["gws"][0]
        end_node_delay_stringhex = data["data"]
        print("end node delay in hex",end_node_delay_stringhex)
        str_time = timetost["time"]
        end_node_delay = int(end_node_delay_stringhex, 16)
        print("network server delay string: ", str_time)
        gateway_server_delay = self.calc_ms(str_time)
        network_serve_delay = (Ts.microsecond / 1000) + (Ts.minute * 60 * 1000) + (Ts.second * 1000)
        print("Network server delay milliseconds: ", network_serve_delay)
        print("gateway server delay milliseconds: ", gateway_server_delay)
        print("end node delay in milliseconds", end_node_delay)
        end_node_network_transmission_delay = ( network_serve_delay - end_node_delay)/1000.0
        end_node_gateway_transmission_delay = ( gateway_server_delay - end_node_delay )/1000.0
        print("end node - gateway trarnsmission delay", end_node_gateway_transmission_delay)
        print("end node - network serve trarnsmission delay", end_node_network_transmission_delay)

        nv4 = datanodesvalue()
        nv4.set_name("Network_delay")
        nv4.set_path("fingerno3")
        nv4.set_dataType("double")
        nv4.set_value(network_serve_delay)
        nv4.set_timestamp(timeStamp)

        nv5 = datanodesvalue()
        nv5.set_name("gateway_delay")
        nv5.set_path("fingerno3")
        nv5.set_dataType("double")
        nv5.set_value(gateway_server_delay)
        nv5.set_timestamp(timeStamp)

        c = Client(self.baseurl, self.username, self.password)

        print(c.writedata("82faafbc015a4f3389f72e0b0d03db10", nv, nv2 ,nv3,nv4,nv5))


    def findMyDevice(self):

        devices = self.c.getdevices()

        for dev in devices.deviceslist:
            if dev.name == self.c.deviceId:
                print("-------------------------------------------------------\n")
                print("Device {} found on server.".format(dev.name))
                print("-------------------------------------------------------\n")
                return dev

        return None

    def calc_ms(self,string):
        rest, millisecond = string.split(".")
        r = ''.join(c for c in millisecond if c != 'Z')
        restr, minute, second = rest.split(":")
        second_to_millisecond = 1000.0 * int(second)
        minute_to_millisecond = 60.0 * int(minute) * 1000
        total_milliseconds = int(r) + minute_to_millisecond + second_to_millisecond
        return total_milliseconds