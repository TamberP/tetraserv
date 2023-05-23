#!/usr/bin/env python3

import configparser
import logging
import argparse
import os, sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import asyncio
import discord
import byond.topic

from bridge import BridgeServerFucktory
config = None

class DiscoClient(discord.Client):

    def __init__(self):
        global config
        our_intents = discord.Intents.default()
        our_intents.message_content = True
        super().__init__(intents=our_intents)

    async def on_ready(self):
        global config
        logging.info('Discord - Connected as {0}'.format(self.user))
        self.announcechan = self.get_channel(int(config['Discord']['Announce']))
        self.logchan = self.get_channel(int(config['Discord']['Logging']))

    async def checkStatus(self, newround=False):
        global config
        # Report the status of the game server.

        # This has to be on localhost because we're part of
        # the bridge, which only works on localhost for
        # security reasons.
        dmServer = config['World']['Host']

        # Port that the game world is running on.
        dmPort = config['World']['Port']

        loop = asyncio.get_running_loop()
        try:
            worldStatus = await loop.run_in_executor(None, byond.topic.queryStatus, dmServer, dmPort)
            if(worldStatus):
                gamedesc = "{0} round {1}, on {2}, with {3} player{4}".\
                    format(worldStatus['mode'][0].title(),
                           ("starting" if (newround) else "in progress"),
                           worldStatus['map_name'][0],
                           worldStatus['players'][0],
                           ("" if (worldStatus['players'][0] == 1) else "s"))

                statusCard = discord.Embed(title="Game Status - {0}".format(worldStatus['version'][0]),
                                           description=gamedesc,
                                           color=discord.Color.blue())
                statusCard.set_footer(text="Join in at: byond://{0}:{1}".format(str(config['World']['Host']),
                                                                                str(config['World']['Port'])))
                return statusCard
            else:
                return discord.Embed(title="Couldn't get game status!",
                                     description="Couldn't get the game status from {0}:{1}!".format(config['World']['Host'],
                                                                                                     config['World']['Port']),
                                     color=discord.Color.red())
        except:
            return discord.Embed(title="Error", description="Shit's fucked yo.", color=discord.Color.red())


    async def on_message(self, message):
        logging.debug('Discord - Message RX')
        if(message.author.id == self.user.id):
            return # Don't listen to ourselves. We just chat shit!

        if((self.user.mentioned_in(message)) or (message.channel.type == discord.ChannelType.private)):
            # Oh! Pay attention!
            if(message.content.find('ping')>0):
                await message.reply('pong!', mention_author=True)

            elif(message.content.find('status')>0):
                async with message.channel.typing():
                    statusCard = await self.checkStatus()
                if(statusCard):
                    await message.reply(embed=statusCard, mention_author=True)
                else:
                    await message.reply("I dunno man...", mention_author=True)


    async def on_disconnect(self):
        logging.info('Discord - Disconnected')

    async def on_error(self, *args, **kwargs):
        logging.error('Discord - Error {0}'.format(sys.exc_info()[1]))

    async def Announce(self, status):
        if(status == 'init'):
            statusCard = await checkStatus(self, True)
            self.announcechan.send(embed=statusCard)
        elif(status == 'reboot'):
            self.announcechan.send("World Rebooting")
        elif(status == 'shutdown'):
            self.announcechan.send("World shutting down")


def main():
    global config
    optP = argparse.ArgumentParser(description="Cheap TetraBridge: Talks crap to BYOND *AND* Discord!")
    optP.add_argument("--loglevel", help="Choose level of logging output.", default="WARN")
    optP.add_argument("--config", "-f", help="Config file to load", default='default.conf')

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
        config.read_file(open(options.config))
    except:
        logging.error("Could not open config: '%s':\n%s", options.config, sys.exc_info()[1])
        sys.exit(1)

    logging.info("Starting...")

    if('Discord' not in config):
        # Woop. Didn't set up yer damn config!
        logging.error("Hey! No discord config set in '%s'!", options.config)
        if('Secret' not in config['Discord'] or config['Discord']['Secret'] == "SET THIS"):
            logging.error("HEY! YOU DIDN'T SET YOUR DISCORD CONFIG PROPERLY")
        sys.exit(1)

    if('World' not in config):
        # Woop! Didn't set up yer damn config!
        logging.error("Hey! No byond world config set in '%s'!", options.config)
        if('Key' not in config['World'] or config['World']['Key'] == "ChangeMe"):
            logging.error("No TGS key set?")
        sys.exit(1)

    daDiscoClient = DiscoClient()

    # Start the bridge thread.
    DaBridgeServer = BridgeServerFucktory(config, daDiscoClient, asyncio.get_event_loop())
    bridge = ThreadingHTTPServer(("127.0.0.1", int(config['TGS']['Port'])), DaBridgeServer)
    bridgeThread = threading.Thread(target=bridge.serve_forever)

    bridgeThread.start()

    daDiscoClient.run(config['Discord']['Secret'])

def checkIdentifier(ident):
    # Check the given ident key against the one from our config.
    return(ident == config['World']['tgs_key'])

if __name__ == '__main__':
    main()

