import http.server

import sys
import urllib
import subprocess


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Received request")

         # parse the query string
        qs = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(qs)

        print(query_components)


class Server:
    def __init__(self):
        print("Starting API Handler")

        # run the server
        server_address = ('', 8000)

        try:
            httpd = http.server.HTTPServer(server_address, Handler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(' received, shutting down server')
            httpd.socket.close()
