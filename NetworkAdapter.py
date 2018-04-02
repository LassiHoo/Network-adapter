import codecs
from iotticket.models import device
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

import datetime
from time import time
import json
import string
from ResultCalculator import result_calculator

class network_adapter:

    username = "LassiPee" #iot-ticket tili
    password = "Lorawandemo1234" #iot-ticket tilin
    baseurl = "https://my.iot-ticket.com/api/v1/"
    deviceId = "testi"
    MEASUREMENT_INTERVAL = 5
    dev1 ="0004A30B001F3A96"
    dev_iot_id = "610ffa1e14b94b8b8bc8079344ab9fae"
    dev2 ="BE7A000000001FF8"
    dev3 ="0004A30B001F3A95"



    def __init__(self):
        self.c = Client(self.baseurl, self.username, self.password)
        print ("network adapter initialized: " + str(self.c))
        self.dev= self.create_device()
        self.dev1_result_calculator = result_calculator()
        self.dev2_result_calculator = result_calculator()
        self.dev3_result_calculator = result_calculator()
        self.dev1 = "0004A30B001F3A96"
        self.dev2 = "BE7A000000001FF8"
        self.dev3 = "0004A30B001F3A95"


    def create_device(self):

        d = device()
        d.set_name("Lorawan end node")
        d.set_manufacturer("Wapice")
        d.set_type("sensor")
        d.set_description("LoRaWAN test network end node")
        d.set_attributes(deviceattribute("packet", "counter"))

        c = Client(self.baseurl, self.username, self.password)

        c.registerdevice(d)
        return c


    def end_node_parser(self,data):

        end_node_address = data["EUI"]
        print("end node address", data["EUI"])
        fingernumber = "EUI" + end_node_address
        print("fingernumber", data["EUI"])
        result = self.parse(end_node_address, data)
        self.write_to_iot_ticket(data, fingernumber,result)

    def parse(self, end_node, data):

        timetost = data["gws"][0]
        print("time",timetost)
        end_node_delay_stringhex = data["data"]
        print("data in hex",end_node_delay_stringhex)
        str_time = timetost["time"]
        e = codecs.decode(end_node_delay_stringhex, "hex")
        ascii = codecs.decode(e, "ascii")
        print("data in ascii", ascii)
        delay, counter, transmission = ascii.split(':')
        input = int(delay), str_time, int(counter), float(transmission)

        if end_node == self.dev1:
            output = self.dev1_result_calculator.calc_result(input)
        if end_node == self.dev2:
            output = self.dev2_result_calculator.calc_result(input)
        if end_node == self.dev3:
            output = self.dev3_result_calculator.calc_result(input)

        return output

    def write_to_iot_ticket(self,data,iot_id,result):

        timeStamp = time()

        rssi = data["gws"][0]
        float_rssi = float(rssi["rssi"])
        nv = datanodesvalue()
        nv.set_name("RSSI")
        nv.set_path(iot_id)
        nv.set_dataType("double")
        nv.set_value(float_rssi)
        nv.set_timestamp(timeStamp)

        gateway_delay = result['gatewaydelay']
        float_gvd = float(gateway_delay)
        nv1 = datanodesvalue()
        nv1.set_name("Gateway delay")
        nv1.set_path(iot_id)
        nv1.set_dataType("double")
        nv1.set_value(float_gvd)
        nv1.set_timestamp(timeStamp)

        network_delay = result['networkdelay']
        float_nvd = float(network_delay)
        nv2 = datanodesvalue()
        nv2.set_name("Network delay")
        nv2.set_path(iot_id)
        nv2.set_dataType("double")
        nv2.set_value(float_nvd)
        nv2.set_timestamp(timeStamp)

        per = result['per']
        float_per = float(per)
        nv3 = datanodesvalue()
        nv3.set_name("PER")
        nv3.set_path(iot_id)
        nv3.set_dataType("double")
        nv3.set_value(float_per)
        nv3.set_timestamp(timeStamp)

        interval = result['interval']
        float_interval = float(interval)
        nv4 = datanodesvalue()
        nv4.set_name("Measurement interval")
        nv4.set_path(iot_id)
        nv4.set_dataType("double")
        nv4.set_value(float_interval)
        nv4.set_timestamp(timeStamp)

        measinterval = result['measinterval']
        float_measinterval = float(measinterval)
        nv5 = datanodesvalue()
        nv5.set_name("Measured interval")
        nv5.set_path(iot_id)
        nv5.set_dataType("double")
        nv5.set_value(float_measinterval)
        nv5.set_timestamp(timeStamp)

        c = Client(self.baseurl, self.username, self.password)

        print(c.writedata(self.dev_iot_id, nv, nv1,nv2, nv3, nv4, nv5 ))


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



