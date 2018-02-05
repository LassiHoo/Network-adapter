import codecs
from iotticket.models import device
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
#import numpy as np
import datetime
from time import time
import json
import string
class network_adapter:

    username = "LassiPee" #iot-ticket tili
    password = "Lorawandemo1234" #iot-ticket tilin
    baseurl = "https://my.iot-ticket.com/api/v1/"
    deviceId = "testi"
    MEASUREMENT_INTERVAL = 5
    dev1 ="0004A30B001F3A96"
    dev2 ="BE7A000000001FF8"
    dev3 ="0004A30B001F3A95"

    def __init__(self):
        self.c = Client(self.baseurl, self.username, self.password)
        print ("network adapter initialized: " + str(self.c))
        self.dev= self.create_device()
        self.packet_counter = 0
        self.packet_err_count = 0
        self.PER = 0
        self.measurement_counter = 0
        self.dev1 = "0004A30B001F3A96"
        self.dev2 = "BE7A000000001FF8"
        self.dev3 = "0004A30B001F3A95"
        self.packet_counter=0
        self.error_counter=0
        self.meas_counter = 0
        self.per_counter = 0

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


    def end_node_parser(self,data):

        end_node_address = data["EUI"]
        print("end node address", data["EUI"])
        fingernumber = "EUI" + end_node_address
        print("fingernumber", data["EUI"])
        self.write_to_iot(data, fingernumber)

    def write_to_iot(self,data,fingernumber):

        print("endnode", fingernumber)
        # pack data to node object

        timetost = data["gws"][0]
        end_node_delay_stringhex = data["data"]
        #print("end node delay in hex",end_node_delay_stringhex)
        str_time = timetost["time"]
        e = codecs.decode(end_node_delay_stringhex, "hex")
        ascii = codecs.decode(e,"ascii")

        if (fingernumber == "EUIBE7A000000001FF8"):

            timeStamp = time()

            rssi = data["gws"][0]
            float_rssi = float(rssi["rssi"])
            # print("rssi: ", float_rssi)
            nv2 = datanodesvalue()
            nv2.set_name("RSSI")
            nv2.set_path(fingernumber)
            nv2.set_dataType("double")
            nv2.set_value(float_rssi)
            nv2.set_timestamp(timeStamp)
            # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
            # nv1.set_timestamp(timeStamp)

            snr = data["gws"][0]
            float_snr = float(snr["snr"])
            print("snr: ", float_snr)
            nv3 = datanodesvalue()
            nv3.set_name("SNR")
            nv3.set_path(fingernumber)
            nv3.set_dataType("double")
            nv3.set_value(float_snr)
            nv3.set_timestamp(timeStamp)
            # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
            # nv1.set_timestamp(timeStamp)
            print(ascii)
            lighthex, temp = ascii.split(' ')
            tempnum = temp[1:4]
            print(tempnum)
            print(lighthex)
            float_ligth = float(lighthex)
            float_temp = float(tempnum)
            print("light  ", float_ligth)
            print("temp  ",  float_temp)

            nv4 = datanodesvalue()
            nv4.set_name("Light")
            nv4.set_path(fingernumber)
            nv4.set_dataType("double")
            nv4.set_value(float_ligth)
            nv4.set_timestamp(timeStamp)

            nv5 = datanodesvalue()
            nv5.set_name("Temp")
            nv5.set_path(fingernumber)
            nv5.set_dataType("double")
            nv5.set_value(float_temp)
            nv5.set_timestamp(timeStamp)

            c = Client(self.baseurl, self.username, self.password)

            print(c.writedata("5c37711ab82d4244bcaa50c071ac94c5", nv2, nv3, nv4, nv5 ))

        if (fingernumber == "EUI0004A30B001F3A95"):

                timeStamp = time()
                Ts = datetime.datetime.now()
                nv = datanodesvalue()
                nv.set_name("Lorawan")
                nv.set_path = (fingernumber)
                nv.set_dataType("double")
                packetcounter = float(data["seqno"])
                print(packetcounter)
                nv.set_value(packetcounter)
                nv.set_timestamp(timeStamp)

                rssi = data["gws"][0]
                float_rssi = float(rssi["rssi"])
                # print("rssi: ", float_rssi)
                nv6 = datanodesvalue()
                nv6.set_name("RSSI")
                nv6.set_path(fingernumber)
                nv6.set_dataType("double")
                nv6.set_value(float_rssi)
                nv6.set_timestamp(timeStamp)
                # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
                # nv1.set_timestamp(timeStamp)

                snr = data["gws"][0]
                float_snr = float(rssi["snr"])
                print("snr: ", float_snr)
                nv7 = datanodesvalue()
                nv7.set_name("SNR")
                nv7.set_path(fingernumber)
                nv7.set_dataType("double")
                nv7.set_value(float_snr)
                nv7.set_timestamp(timeStamp)
                # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
                # nv1.set_timestamp(timeStamp)
                print(ascii)
                lighthex, temp = ascii.split(' ')
                tempnum = temp[1:4]
                print(tempnum)
                print(lighthex)
                float_ligth = float(lighthex)
                float_temp = float(tempnum)
                print("light  ", float_ligth)
                print("temp  ", float_temp)

                nv8 = datanodesvalue()
                nv8.set_name("Light")
                nv8.set_path(fingernumber)
                nv8.set_dataType("double")
                nv8.set_value(float_ligth)
                nv8.set_timestamp(timeStamp)

                nv9 = datanodesvalue()
                nv9.set_name("Temp")
                nv9.set_path(fingernumber)
                nv9.set_dataType("double")
                nv9.set_value(float_temp)
                nv9.set_timestamp(timeStamp)

                c = Client(self.baseurl, self.username, self.password)

                print(c.writedata("5c37711ab82d4244bcaa50c071ac94c5", nv6, nv7, nv8, nv9 ))

        if (fingernumber == "EUI0004A30B001F3A96"):
            timeStamp = time()
            Ts = datetime.datetime.now()
            nv = datanodesvalue()
            nv.set_name("Lorawan")
            nv.set_path = ("fingerno1")
            nv.set_dataType("double")
            packetcounter = float(data["seqno"])
            print(packetcounter)
            nv.set_value(packetcounter)
            nv.set_timestamp(timeStamp)

            rssi = data["gws"][0]
            float_rssi = float(rssi["rssi"])
            # print("rssi: ", float_rssi)
            nv2 = datanodesvalue()
            nv2.set_name("RSSI")
            nv2.set_path(fingernumber)
            nv2.set_dataType("double")
            nv2.set_value(float_rssi)
            nv2.set_timestamp(timeStamp)
            # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
            # nv1.set_timestamp(timeStamp)

            snr = data["gws"][0]
            float_snr = float(rssi["snr"])
            print("snr: ", float_snr)
            nv3 = datanodesvalue()
            nv3.set_name("SNR")
            nv3.set_path(fingernumber)
            nv3.set_dataType("double")
            nv3.set_value(float_snr)
            nv3.set_timestamp(timeStamp)
            # bugi kirjastossa tämä pitäisi tulla automaattisesti, ei tule!
            # nv1.set_timestamp(timeStamp)

            delay, counter, transmission = ascii.split(':')
            end_node_delay = int(delay)
            end_nodecounter = int(counter)
            transmission_interval = float(transmission)
            #print("gateway server delay string: ", str_time)
            #print("network server delay string: ", Ts)
            gateway_server_delay = self.calc_ms(str_time)
            network_serve_delay = (Ts.microsecond / 1000) + (Ts.minute * 60 * 1000) + (Ts.second * 1000)
            #print("Network server delay milliseconds: ", network_serve_delay)
            #print("gateway server delay milliseconds: ", gateway_server_delay)
            #print("end node delay in milliseconds", end_node_delay)
            end_node_network_transmission_delay = network_serve_delay - end_node_delay
            end_node_gateway_transmission_delay = gateway_server_delay - end_node_delay
            #print("end node - gateway trarnsmission delay", end_node_gateway_transmission_delay)
            #print("end node - network serve trarnsmission delay", end_node_network_transmission_delay)
            #print("end node sequence number ", end_nodecounter )
                    #print("Transmission interval  ", transmission_interval)

            if ( self.packet_counter != 0):
                if end_nodecounter != (self.packet_counter + 1):
                    self.error_counter= self.error_counter + 1.0
                self.meas_counter = self.meas_counter + 1
                if self.meas_counter == self.MEASUREMENT_INTERVAL :
                    self.per_counter = ( self.error_counter / self.meas_counter )
                    self.error_counter = 0
                    self.meas_counter = 0
            derivate =  end_nodecounter - self.packet_counter

            print("derivate  ", derivate)
            print("end node counter  ", end_nodecounter)
            self.packet_counter = end_nodecounter
            print("packet counter  ", self.packet_counter)
            print("derivate  ", derivate)
            print("end node counter  ", end_nodecounter)
            print("packet counter  ", self.packet_counter)
            print("packet error counter  ", self.error_counter)
            print("packet meas counter  ", self.meas_counter)
            print("per  ", self.per_counter)

            nv4 = datanodesvalue()
            nv4.set_name("Network_delay")
            nv4.set_path(fingernumber)
            nv4.set_dataType("double")
            nv4.set_value(end_node_network_transmission_delay)
            nv4.set_timestamp(timeStamp)

            nv5 = datanodesvalue()
            nv5.set_name("gateway_delay")
            nv5.set_path(fingernumber)
            nv5.set_dataType("double")
            nv5.set_value(end_node_gateway_transmission_delay)
            nv5.set_timestamp(timeStamp)

            nv6 = datanodesvalue()
            nv6.set_name("PER")
            nv6.set_path(fingernumber)
            nv6.set_dataType("double")
            nv6.set_value(self.per_counter)
            nv6.set_timestamp(timeStamp)

            nv17 = datanodesvalue()
            nv17.set_name("derivate")
            nv17.set_path(fingernumber)
            nv17.set_dataType("double")
            nv17.set_value(derivate)
            nv17.set_timestamp(timeStamp)

            nv18 = datanodesvalue()
            nv18.set_name("Tx_interval")
            nv18.set_path(fingernumber)
            nv18.set_dataType("double")
            nv18.set_value(transmission_interval)
            nv18.set_timestamp(timeStamp)

            c = Client(self.baseurl, self.username, self.password)

            print(c.writedata("5c37711ab82d4244bcaa50c071ac94c5", nv, nv2 ,nv3,nv4,nv5,nv6,nv17,nv18))


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
        #print("calc_millisecond string",string)
        rest, millisecond = string.split(".")
        r = ''.join(c for c in millisecond if c != 'Z')
        restr, minute, second = rest.split(":")
        #print("second string", second)
        second_to_millisecond = 1000.0 * int(second)
        #print("second to millisecond", second_to_millisecond)
        #print("minute string", minute)
        minute_to_millisecond = 60.0 * int(minute) * 1000
        #print("minute to millisecond", minute_to_millisecond)
        total_milliseconds = int(r)/1000 + minute_to_millisecond + second_to_millisecond
        #print("total millisecond", total_milliseconds)
        return total_milliseconds

    # def ccdf(self, datain):
    #     cdfx = np.sort(datain)
    #     cdfy = np.linspace(1 / len(datain), 1.0, len(datain))
    #     return cdfx, cdfy