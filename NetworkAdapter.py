from iotticket.client import Client
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

class network_adapter:

    username = "LassiPee" #iot-ticket tili
    password = "Lorawandemo1234" #iot-ticket tilin
    baseurl = "https://my.iot-ticket.com/api/v1/"
    c = Client(baseurl, username, password)
    deviceId = "testi"

    def __init__(self):
        c = Client(self.baseurl, self.username, self.password)

    def create_device(self):
        #create device
        if (self.c != "404 URL NOT FOUND!!!"):

            d = self.device()
            d.set_name("LoraWan network adapter")
            d.set_manufacturer("Wapice")

            print(self.c.registerdevice(d))

        else:
            print(self.c)


    def write_to_iot(self,data):

        nv1 = add_node("data", data["EUI"], "string", data["data"])  # helppo käyttää EUI:ta polkuna, tällä tavoin
        # siis vain kirjoitetaan suoraan hex payload iot-ticketiin ja halutessa se pitää vielä parsia ennen kirjoitusta ja kirjoittaa parsittu data mahdollisesti useampaan datanodeen
        print(self.c.writedata(self.deviceId, nv1))

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self):

        self.iot_ticket = network_adapter()
        self.server = HTTPServer(('', port), RequestHandler)

    def do_GET(self):
        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")

        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()

    def do_POST(self):
        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)

        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0

        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", self.rfile.read(length))
        print("<----- Request End -----\n")
        self.iot_ticket.write_to_iot(self.self.rfile.read(length))
        self.send_response(200)
        self.end_headers()

    do_PUT = do_POST
    do_DELETE = do_GET