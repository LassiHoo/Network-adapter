from iotticket.client import Client
from iotticket.models import datanodesvalue
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
import numpy as np
import datetime
from time import time
import json
class network_adapter:

    username = "LassiPee" #iot-ticket tili
    password = "Lorawandemo1234" #iot-ticket tilin
    baseurl = "https://my.iot-ticket.com/api/v1/"
    deviceId = "testi"
    MEASUREMENT_INTERVAL = 5

    def __init__(self):
        self.c = Client(self.baseurl, self.username, self.password)
        print ("network adapter initialized: " + str(self.c))
        self.dev= self.create_device()
        self.packet_counter = 0
        self.packet_err_count = 0
        self.PER = 0
        self.measurement_counter = 0


    def create_device(self):

        d = device()
        d.set_name("Lorawan end node")
        d.set_manufacturer("Wapice")
        d.set_type("employee")
        d.set_description("Im trainee")
        d.set_attributes(deviceattribute("packet", "counter"))

        c = Client(self.baseurl, self.username, self.password)

        c.registerdevice(d)
        return c


    def write_to_iot(self,data):

        # pack data to node object
        timeStamp = time()
        Ts = datetime.datetime.now()
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
        print("gateway server delay string: ", str_time)
        print("network server delay string: ", Ts)
        gateway_server_delay = self.calc_ms(str_time)
        network_serve_delay = (Ts.microsecond / 1000) + (Ts.minute * 60 * 1000) + (Ts.second * 1000)
        print("Network server delay milliseconds: ", network_serve_delay)
        print("gateway server delay milliseconds: ", gateway_server_delay)
        print("end node delay in milliseconds", end_node_delay)
        end_node_network_transmission_delay = network_serve_delay - end_node_delay
        end_node_gateway_transmission_delay = gateway_server_delay - end_node_delay
        print("end node - gateway trarnsmission delay", end_node_gateway_transmission_delay)
        print("end node - network serve trarnsmission delay", end_node_network_transmission_delay)
        sequencenumber = int(data["seqno"])
        print("sequence number ", sequencenumber  )
        print("packet counter  ", self.packet_counter)
        print("packet error counter  ", self.packet_err_count)
        print("packet meas counter  ", self.measurement_counter)
        if ( self.packet_counter != 0):
            if sequencenumber != (self.packet_counter + 1):
                self.packet_err_count = self.packet_err_count + 1.0
            self.measurement_counter = self.measurement_counter + 1
            if self.measurement_counter == self.MEASUREMENT_INTERVAL :
                self.PER = ( self.packet_err_count / self.packet_counter ) * 100.0
                self.packet_err_count = 0
                self.measurement_counter = 0
        self.packet_counter = sequencenumber
        print("PER ",self.PER)


        nv4 = datanodesvalue()
        nv4.set_name("Network_delay")
        nv4.set_path("fingerno2")
        nv4.set_dataType("double")
        nv4.set_value(end_node_network_transmission_delay)
        nv4.set_timestamp(timeStamp)

        nv5 = datanodesvalue()
        nv5.set_name("gateway_delay")
        nv5.set_path("fingerno2")
        nv5.set_dataType("double")
        nv5.set_value(end_node_gateway_transmission_delay)
        nv5.set_timestamp(timeStamp)

        nv16 = datanodesvalue()
        nv16.set_name("Err_count")
        nv16.set_path("fingerno2")
        nv16.set_dataType("double")
        nv16.set_value(self.packet_err_count)
        nv16.set_timestamp(timeStamp)

        nv17 = datanodesvalue()
        nv17.set_name("PER")
        nv17.set_path("fingerno2")
        nv17.set_dataType("double")
        nv17.set_value(self.PER)
        nv17.set_timestamp(timeStamp)

        nv18 = datanodesvalue()
        nv18.set_name("CCDFX")
        nv18.set_path("fingerno2")
        nv18.set_dataType("double")
        nv18.set_value(self.PER)
        nv18.set_timestamp(timeStamp)

        nv19 = datanodesvalue()
        nv19.set_name("CCDFY")
        nv19.set_path("fingerno2")
        nv19.set_dataType("double")
        nv19.set_value(self.PER)
        nv19.set_timestamp(timeStamp)


        c = Client(self.baseurl, self.username, self.password)

        print(c.writedata("b57b22d0c44f4688a89933ecb7de5637", nv, nv2 ,nv3,nv4,nv5,nv16,nv17))


    # def findMyDevice(self):
    #
    #     devices = self.c.getdevices()
    #
    #     for dev in devices.deviceslist:
    #         if dev.name == self.c.deviceId:
    #             print("-------------------------------------------------------\n")
    #             print("Device {} found on server.".format(dev.name))
    #             print("-------------------------------------------------------\n")
    #             return dev
    #
    #     return None

    def calc_ms(self,string):
        print("calc_millisecond string",string)
        rest, millisecond = string.split(".")
        r = ''.join(c for c in millisecond if c != 'Z')
        restr, minute, second = rest.split(":")
        print("second string", second)
        second_to_millisecond = 1000.0 * int(second)
        print("second to millisecond", second_to_millisecond)
        print("minute string", minute)
        minute_to_millisecond = 60.0 * int(minute) * 1000
        print("minute to millisecond", minute_to_millisecond)
        total_milliseconds = int(r)/1000 + minute_to_millisecond + second_to_millisecond
        print("total millisecond", total_milliseconds)
        return total_milliseconds

    def ccdf(self, datain):
        cdfx = np.sort(datain)
        cdfy = np.linspace(1 / len(datain), 1.0, len(datain))
        return cdfx, cdfy