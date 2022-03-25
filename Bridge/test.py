#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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
        "channels": [
            {
                "id": 0,
                "friendly_name": "Channel",
                "connection_name": "conn.test",
                "isAdminChannel": False,
                "isPrivateChannel": False,
                "tag": "Boop"
             }
        ]
    }
}

class BridgeServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        req = urllib.parse.urlparse(self.path)
        req = urllib.parse.parse_qs(req.query)

        # Bridge command data is always passed in 'data'=<whatever>
        tgs_data = json.loads(req["data"][0])
        commandType = tgs_data["commandType"]

        # See the DMAPI5 defines
        if commandType == 0:
            print("Port Update Request")
        elif commandType == 1:
            print("Start-Up Sequence")
            # Yeah, just fake it
            self.wfile.write(bytes(json.dumps(dumb_response), "utf-8"))
        elif commandType == 2:
            print("Primed: Initialisation Complete")
        elif commandType == 3:
            print("Reboot request")
            # At this point, we'd tell the watchdog to send SIGUSR1 to the DreamDaemon process.
        elif commandType == 4:
            print("Kill request")
            # Tell the watchdog to go into shutdown mode.
        elif commandType == 5:
            print("Chat Send:")
            print(tgs_data["chatMessage"]["text"])
        else:
            print("Unknown command: %s" % str(commandType))

        if "accessIdentifier" in tgs_data:
            print("Key given: %s" % tgs_data["accessIdentifier"])

    # Shh
    def log_message(self, format, *args):
        print("*")
        pass


if __name__ == "__main__":
    webServer = ThreadingHTTPServer(("localhost", 26263), BridgeServer)
    print("Server started!")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
