from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import time
import json
import urllib.parse
import logging
import asyncio
import subprocess

def BridgeServerFucktory(conf, comms, otherloop):
    class BridgeServer(BaseHTTPRequestHandler):
        tgsApiVersion = "5.2.4"
        config = conf
        discrod = comms
        evloop = otherloop

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()

            # TGS Bridge requests are HTTP requests with all the good
            # stuff in an urlencoded query string.
            req = urllib.parse.urlparse(self.path)
            req = urllib.parse.parse_qs(req.query)

            # Bridge command data is json passed in 'data'=<whatever>
            tgsData = json.loads(req["data"][0])
            commandType = tgsData["commandType"]
            if 'accessIdentifier' in tgsData:
                # check it against the one it's supposed to be
                if(tgsData['accessIdentifier'] != self.config['TGS']['Key']):
                    logging.warning("Bridge: Incorrect TGS key received: '{0}' is not '{1}'".format(tgsData['accessIdentifier'], self.config['TGS']['Key']))
                    return
            else:
                logging.warning("Bridge: No TGS key received")

                # It should also pass, in tgsData["accessIdentifier"], the
                # authentication key passed as part of the server's param
                # string when DreamDaemon was started.

                # DMAPI5 defines are worth a look at.
            if commandType == 0:
                    # Port update request. We can't do anything about that.
                pass
            elif commandType == 1:
                # World start-up sequence. The world wants the runtime information:
                # - The DMAPI version it should use to communicate
                # - The security level it's running at
                # - The name of the instance
                # - Revision info
                #   + SHA hash of the git commit the world was built from
                #   + origin/master of the git repo
                # - Something called 'testMerges'. Not quite sure on this.
                # - A list of the communication channels available to communicate by
                #   + ID
                #   + Friendly Name
                #   + Connection Name
                #   + Admin channel?
                #   + Private channel?
                #   + Custom Tag
                runtimeResponse = {
                    "runtimeInformation": {
                        "serverVersion": self.tgsApiVersion,
                        "securityLevel": 0,
                        "instanceName":  "ChangeMe XXX",
                        "revision":
                        {
                            "commitSha": 'sha hash here',
                            "originCommitSha": 'another sha hash here'
                        },
                        "testMerges": [],
                        "channels": []
                    }
                }
                self.wfile.write(bytes(json.dumps(runtimeResponse), "utf-8"))
            elif commandType == 2:
                # World primed. Initialisation complete.
                logging.info("Bridge: World initialisation complete.")
                asyncio.run_coroutine_threadsafe(self.discrod.Announce('init'), self.evloop)
            elif commandType == 3:
                logging.info("Bridge: World requests reboot")
            elif commandType == 4:
                logging.info("Bridge: World requests shutdown.")
            elif commandType == 5:
                # Chat send.
                logging.debug("Bridge: Chat send")
                # tgs_data["chatMessage"] contains json with:
                # - 'text':       The message
                # - 'channelIds': A list of IDs of which channels the message is to be sent to.
                #                 These refer to the channels given in the runtimeInformation.
                #
                # These messages are called by one of:
                # * ChatBroadcast
                #    Sends to all channels listed in runtimeInformation
                # * ChatTargetedBroadcast (Optionally admin-only)
                #    Sends to all non-private channels excluding admin-only,
                #    or to all admin-only channels if admin-only is set.
                # * ChatPrivateMessage (Directed to a specific chat user)
                #    Channel ID = user.channel.id
                pass
            else:
                # Unknown command.
                logging.warn("Unknown Bridge Command Received: Type: " + str(commandType) + ".")

        def log_message(self, format, *args):
                    logging.debug("Bridge request received")

    return BridgeServer
