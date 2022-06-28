#!/usr/bin/env python3

import configparser
import logging
import argparse
import os, sys
import time

global config
global disco
global bridge

def main:
    optP = argparse.ArgumentParser(description="Cheap TetraBridge: Talks crap to BYOND *AND* Discord!")
    optP.add_argument("--loglevel", help="Choose level of logging output.", default="INFO")
    optP.add_argument("--config", "-f", help="Config file to load", default="default.conf")

    options = optP.parse_args()
    if(options.loglevel):
        log_level_num = getattr(logging, options.loglevel.upper(), None)
        if not isinstance(log_level_num, int):
            logging.warning("Invalid log level: %S", log_level_num)
            sys.exit(-1)
        else:
            logging.basicConfig(level=log_level_num)
    else:
        logging.basicConfig(level=log_level_num)

    config = configparser.ConfigParser()
    try:
        config.read_file(options.config)
    except:
        logging.error("Could not open config: '%s':\n%s", options.config, sys.exc_info()[1])
        sys.exit(1)

    if('Discord' not in config):
        # Woop. Didn't set up yer damn config!
        logging.error("Hey! No discord config set in '%s'!", options.config)
        sys.exit(1)

    if('World' not in config):
        # Woop! Didn't set up yer damn config!
        logging.error("Hey! No byond world config set in '%s'!", options.config)
        sys.exit(1)

    # Start the bridge thread.

    # Start the discord thread.

def checkIdentifier(ident):
    # Check the given ident key against the one from our config.
    return(ident == config['World']['tgs_key'])

if __name__ == '__main__':
    main()
