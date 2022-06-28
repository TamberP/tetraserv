import discord
import byond.topic
import logging

class DiscoClient(discord.Client):
    async def on_ready(self):
        logging.info('Discord - Connected as {0}'.format(self.user))

    async def on_message(message):
        if(message.author == self.user):
            return # Don't listen to ourselves. We just chat shit!

        if(self.user in message.mentions):
            # Oh! Pay attention!
            if(message.content.startswith('status')):
               # Report the status of the game server.
                dmServer = 'localhost' # This has to be on localhost,
                                      # because we're part of the
                                      # bridge which only works on
                                      # localhost for security
                                      # reasons.

                dmPort = int(42069) # Port that the game world is
                                    # running on.

                worldStatus = byond.topic.queryStatus(dmServer, dmPort)
                if(worldStatus):
                    statusCard = discord.Embed(title="Game Status - {0}".format(status['version']),
                                               url="byond://fusilli.coolstation.space:8085",
                                               description="{0} round in progress, on {1}, with {2} players".format(\
                                                    status['mode'], status['map_name'], status['players']),
                                               color: discord.Color.blue())
                    
                    statusCard.add_field
                    await ctx.send(embed=statusCard)
                    # Currently playing status['mode'], with status['players'] on status['map_name']

    async def on_disconnect(self):
        logging.info('Discord - Disconnected')

    async def on_error(event):
        logging.error('Discord - Error {0}'.format(sys.exc_info()[1]))
