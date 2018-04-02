import numpy as np
import datetime

class result_calculator:


    def __init__(self):
        self.per_counter = 0
        self.error_counter = 0
        self.meas_counter = 0
        self.gateway_cdf_buffer=[]
        self.network_cdf_buffer = []
        self.MEASUREMENT_INTERVAL = 20
        self.CDF_MEASUREMENT_INTERVAL = 100
        self.network_delay
        self.gateway_cdf_result_buffer = {}
        self.network_cdf_result_buffer = {}
        self.data = {}
        self.data['result'] = []
        self.data['result'].append({
            'start_time': 'none',
            'per': self.per_counter,
            'cdf': self.cdf_buffer,
            'gatewaydelay': self.gateway_delay,
            'networkdelay': self.network_delay,
            'gatewaydelay_cdf': self.gateway_cdf_buffer,
            'network_cdf': self.network_cdf_buffer,
        })

    def cdf_calculation(self, samplebuffer):
        if len(samplebuffer)==self.CDF_MEASUREMENT_INTERVAL:
            del samplebuffer[:]
        cdfx = np.sort(samplebuffer)
        cdfy = np.linspace(1 / len(samplebuffer), 1.0, len(samplebuffer))
        return cdfx, cdfy


    def per_calculator(self, end_nodecounter):
        if ( self.packet_counter != 0):
            if end_nodecounter != (self.packet_counter + 1):
                self.error_counter= self.error_counter + 1.0
            self.meas_counter = self.meas_counter + 1
            if self.meas_counter == self.MEASUREMENT_INTERVAL:
                self.per_counter = ( self.error_counter / self.meas_counter )
                self.error_counter = 0
                self.meas_counter = 0

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
        self.delay = total_milliseconds

    def calc_result(self,input):
        Ts = datetime.datetime.now()
        end_node_delay = self.calc_ms(input.end_node_delay)
        network_server_delay = (Ts.microsecond / 1000) + (Ts.minute * 60 * 1000) + (Ts.second * 1000)
        gateway_server_delay = self.calc_ms(input.gateway_delay)
        # print("Network server delay milliseconds: ", network_serve_delay)
        # print("gateway server delay milliseconds: ", gateway_server_delay)
        # print("end node delay in milliseconds", end_node_delay)
        self.data['result']['gatewaydelay'] = gateway_server_delay - end_node_delay
        self.data['result']['networkdelay'] = network_server_delay - end_node_delay
        self.per_counter(input.packet_counter)
        self.gateway_cdf_buffer.append(self.data['result']['gatewaydelay'])
        self.gateway_cdf_result_buffer=self.cdf_calculation(self.gateway_cdf_buffer)
        self.network_cdf_buffer.append(self.data['result']['networkdelay'])
        self.network_cdf_result_buffer=self.cdf_calculation( self.network_cdf_buffer )

        return self.data