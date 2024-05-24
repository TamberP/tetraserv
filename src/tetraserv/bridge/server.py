import tetraserv
import tetraserv.util.git
import tetraserv.comms

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import urllib.parse
import logging

class BridgeHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logging.debug("Bridge: Received request")

    def do_GET(self):
        req = urllib.parse.urlparse(self.path)
        req = urllib.parse.parse_qs(req.query)

        tgsData = json.loads(req["data"][0])
        commandType = tgsData["commandType"]

        tserv = tetraserv.getTetra()

        if 'accessIdentifier' in tgsData:
            # Check the given key against the one that the server was started with.
            if(tserv.checkIdentifier(tgsData['accessIdentifier'])):
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()
            else:
                # Nah, buddy
                logging.warning("Bridge: Incorrect TGS key received")
                self.send_response(403)
                self.end_headers()
                return
        else:
            self.send_response(403)
            self.end_headers()
            logging.warning("Bridge: No TGS key received")
            return

        if commandType == 0:
            # Port update request.
            logging.info("Bridge: World requests port update")
            pass
        elif commandType == 1:
            # Start-up Sequence/Initial Bridge comms
            # Construct a response runtimeInformation
            response = {
                "runtimeInformation": {
                    "serverVersion": tserv.apiVersion(),
                    "securityLevel": tserv.securityLevel(),
                    "instanceName": tserv.name(),
                    "revision": {
                        "commitSha": tetraserv.util.git.getHash(tetraserv.getTetra()),
                        "originCommitSha": tetraserv.util.git.getUpstreamHash(tetraserv.getTetra())
                    },
                    "testMerges": [], #tmp
                    "channels": tserv.comms.getChannels(),
                }
            }

            self.wfile.write(bytes(json.dumps(response), "utf-8"))
            tserv.bridge.worldStart()
        elif commandType == 2:
            # Primed: World initialisation complete.
            # (use this to, perhaps, announce the new round in your discord or whatnot.)
            logging.info("Bridge: World initialisation complete.")
            tserv.bridge.worldPrimed()
            pass
        elif commandType == 3:
            logging.info("Bridge: World rebooting.")
            tserv.bridge.worldReboot()
            pass
        elif commandType == 4:
            # Kill request. (Watchdog to go to shutdown mode.)
            logging.info("Bridge: World requests killing.")
            tserv.bridge.worldKill()
            pass
        elif commandType == 5:
            # Chat send
            logging.debug("Bridge: Chat send.")
            # tgs_data["chatMessage"] contains json with:
            # - text : The message
            # - channelIds: IDs of the channels the message is to be sent to.
            tserv.comms.worldchat(tgsData["chatMessage"])
            tserv.bridge.worldChat()
            pass
