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
    dev_iot_id = "5c37711ab82d4244bcaa50c071ac94c5"
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
        result = self.multiplex(end_node_address,data)
        self.write_to_iot_ticket(data, fingernumber,result)

    def multiplex(self,end_node,data):

        timetost = data["gws"][0]
        end_node_delay_stringhex = data["data"]
        # print("end node delay in hex",end_node_delay_stringhex)
        str_time = timetost["time"]
        e = codecs.decode(end_node_delay_stringhex, "hex")
        ascii = codecs.decode(e, "ascii")

        delay, counter, transmission = ascii.split(':')
        input.end_node_delay = int(delay)
        input.gateway_delay = str_time
        input.end_nodecounter = int(counter)
        input.transmission_interval = float(transmission)

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
        # print("rssi: ", float_rssi)
        nv = datanodesvalue()
        nv.set_name("RSSI")
        nv.set_path(iot_id)
        nv.set_dataType("double")
        nv.set_value(float_rssi)
        nv.set_timestamp(timeStamp)

        timeStamp = time()

        gateway_delay = result['result']['gatewaydelay']
        float_rssi = float(gateway_delay)
        # print("rssi: ", float_rssi)
        nv1 = datanodesvalue()
        nv1.set_name("Gateway delay")
        nv1.set_path(iot_id)
        nv1.set_dataType("double")
        nv1.set_value(float_rssi)
        nv1.set_timestamp(timeStamp)

        c = Client(self.baseurl, self.username, self.password)

        print(c.writedata(self.dev_iot_id, nv, nv1 ))


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



