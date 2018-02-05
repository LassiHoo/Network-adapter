#!/usr/bin/env python
#

from NetworkAdapter import network_adapter
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import codecs

class RequestHandler(BaseHTTPRequestHandler):


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
        payload =  self.rfile.read(length)
        print("Request payload:", payload)
        reply = json.loads(payload.decode())
        print("decoded EUI reply", reply["EUI"])
        print("<----- Request End -----\n")
        self.send_response(200)
        self.end_headers()
        iot_ticket.end_node_parser(reply)

    do_PUT = do_POST
    do_DELETE = do_GET


def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler )
    server.serve_forever()
    network_adapter.create_device()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    iot_ticket = network_adapter()
    main()
