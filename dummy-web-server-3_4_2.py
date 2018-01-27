#!/usr/bin/env python
#

from optparse import OptionParser
from NetworkAdapter import RequestHandler


def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    
    network_adapter.server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    network_adapter = RequestHandler()
    main()
