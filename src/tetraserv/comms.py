import tetraserv
import logging

class Comms:
    def __init__(self, config):
        pass

    def shutdown(self):
        logging.info('Comms - Shutting down')

    def getChannels(self):
        return [ ] # XXX: tmp

    def worldChat(self, message):
        # Given a tgs_data["chatMessage"], figure out where it's going
        # to and get it forwarded on. Empty channelIds list means it's
        # being sent to all.
        #
        # {'text': 'Message text', 'channelIds': []}
        pass
