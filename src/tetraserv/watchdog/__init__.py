import tetraserv
import logging
import asyncio
import signal
import urllib
import os.path

class Watchdog:
    def __init__(self, config):
        self.config = config
        self.Tetra = tetraserv.getTetra()

    def shutdown(self):
        # Sends signal.SIGTERM to the process, which DreamDaemon traps
        # in order to perform a graceful shutdown.
        self.dream.terminate()

    async def start(self):
        await self.dream.run()

    def reboot(self):
        # Sends SIGUSR1 to the process, which DreamDaemon uses to perform
        # a reboot of the world.
        self.dream.send_signal(signal.SIGUSR1)

    def kill(self):
        self.dream.kill()

    def main(self):
        # At this point, we should know where the byond executables
        # are, what dmb file we're using and where it is, and so
        # forth.

        # Parameters to hand over to DM in the param list:
        # - 'server_service_version': What's our API version?
        #
        # - 'tgs_port': What port is the Bridge server running on?
        #
        # - 'tgs_key': Authentication key for comms between the World
        # and the Bridge server/in authenticated Topic calls.
        #
        # We assemble all our ducks in a row thusly:
        #
        # <dmb name> -port <port> -close -logself -[trusted|safe|ultrasafe] [-log <filename>] -params <parameters>
        #
        # Then, we hand it all over onto the subprocess, let it do its
        # thing, and wait for it to complete. (Also, catch any stderr/stdout and shove it into a logfile maybe?)
        parameters = {
            'server_service_version': self.Tetra.apiVersion(),
            'tgs_port': self.config['Bridge']['port'],
            'tgs_key': self.config['Server']['tgs_key']
        }

        paramstring = urllib.parse.urlencode(parameters)
        args = [
            os.path.join(self.config['World']['directory'], self.config['World']['name']),
            self.config['World']['port'],
            "-{0}".format(self.Tetra.securityLevelStr()),
            "-params {0}".format(paramstring)
        ]

        self.dream = asyncio.create_subprocess_exec(self.Tetra.dreamDaemonBin(), *args)

        asyncio.run(self.dream)
        pass
