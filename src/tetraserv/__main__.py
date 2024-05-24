import sys
import tetraserv
import logging
import argparse

if __name__ == '__main__':
    optP = argparse.ArgumentParser(prog="ts.sh",
                                   description="TetraServ: Like tgstation-server, but simpler and stupider")
    optP.add_argument("--loglevel", help="Choose level of logging output")
    optP.add_argument("--config", "-f", help="Config file to load", default="")

    options = optP.parse_args()

    if(options.loglevel):
        log_level_num = getattr(logging, options.loglevel.upper(), None)
        if not isinstance(log_level_num, int):
            logging.warning("Invalid log level: %s", log_level_num)
            sys.exit(-1)
        else:
            logging.basicConfig(level=log_level_num)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        ts=tetraserv.TetraServ(options.config)
        ts.main()
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt received: Shutting down")
        ts.shutdown()
