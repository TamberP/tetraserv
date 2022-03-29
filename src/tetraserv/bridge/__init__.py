import tetraserv
from http.server import HTTPServer
from tetraserv.bridge.server import BridgeHandler
import logging


class Bridge:
    def __init__(self, config):
        self.server = HTTPServer((config['Bridge']["address"], int(config['Bridge']["port"])), BridgeHandler)

    def shutdown(self):
        logging.info('Bridge - Shutting down')
        self.server.shutdown()

    # 'callbacks', to be overridden for if you want to do things on these events, I guess?
    def worldStart(self):
        pass

    def worldPrimed(self):
        pass

    def worldReboot(self):
        pass

    def worldKill(self):
        pass

    def worldChat(self):
        pass

    # start the thumbtwiddling
    def main(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.shutdown()
