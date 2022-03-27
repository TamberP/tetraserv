import configparser
import os, sys
import threading, asyncio
import time
import logging
from tetraserv.bridge import Bridge
from tetraserv.comms import Comms
from tetraserv.watchdog import Watchdog

global tserv

def getTetra():
    global tserv
    return tserv

def _setTetra(tetra):
    global tserv
    tserv = tetra

class TetraServ:

    flag = { }

    def __init__(self, configFile):
        # Read configs, set things up (like git repo stuff if required), and whatnot.
        self.config = configparser.ConfigParser()
        if(configFile == ""):
            configFile = 'Default.conf'
        try:
            self.config.read_file(open(configFile))
        except:
            logging.error("Could not open config: '%s':\n%s", configFile, sys.exc_info()[1])
            sys.exit(1)

        if('Git' in self.config):
            self.flag['Git'] = True
        if('Discord' in self.config):
            self.flag['Discord'] = True
        _setTetra(self)

    def checkIdentifier(self, ident):
        # Check the given ident key against the one passed to DreamDaemon
        return(ident == self.config['Server']['tgs_key'])

    def securityLevel(self):
        # Return what security level we're currently operating under.
        return 0 # XXX: tmp

    def securityLevelStr(self):
        if(self.securityLevel() == 0):
            return "trusted"
        elif(self.securityLevel() == 1):
            return "safe"
        else:
            return "ultrasafe"

    def name(self):
        # Name of this server instance
        return "TetraStation13"

    def apiVersion(self):
        return "5.2.4"

    def shutdown(self):
        self.watchdog.shutdown()
        self.bridge.shutdown()
        self.comms.shutdown()

    def dreamDaemonBin(self):
        return "/home/tamber/opt/byond/bin/DreamDaemon" # temporary

    def main(self):
        logging.info('Bridge - Starting')
        try:
            self.bridge = Bridge(self.config)
            self.bridgeThread = threading.Thread(target=self.bridge.main)
            self.bridgeThread.start()
        except:
            logging.error('Bridge - Failed to start: {0}'.format(sys.exc_info()[1]))
            self.shutdown()

        logging.info('Comms - Starting')
        try:
            if('Comms' not in self.config):
                self.config['Comms'] = []

            self.comms = Comms(self.config)
        except:
            logging.error('Comms - Failed to start: {0}'.format(sys.exc_info()[1]))
            self.shutdown()

        logging.info('Watchdog - Starting')
        try:
            self.watchdog = Watchdog(self.config)
            self.watchdogThread = threading.Thread(target=self.watchdog.main)
            self.watchdogThread.start()
        except:
            logging.error('Watchdog - Failed to start: {0}'.format(sys.exc_info()[1]))

        while True:
            time.sleep(0.5)
