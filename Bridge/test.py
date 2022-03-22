#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import urllib.parse

dumb_response = {
    "runtimeInformation": {
        "serverVersion": "5.2.4",
        "securityLevel": 0,
        "instanceName": "Testing",
        "revision": {"commitSha": '70bc0ae0e8e4f3c85a79b4085eedf44123e3602c',
                     "originCommitSha": '70bc0ae0e8e4f3c85a79b4085eedf44123e3602c'},
        "testMerges": [],
        "chatChannels": []
    }
}

class BridgeServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        self.wfile.write(bytes(json.dumps(dumb_response), "utf-8"))

        req = urllib.parse.urlparse(self.path)
        req = urllib.parse.parse_qs(req.query)

        # Bridge command data is always passed in 'data'=<whatever>
        tgs_data = json.loads(req["data"][0])
        print("Server API version: %s" % tgs_data["version"])


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 26263), BridgeServer)
    print("Server started!")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
