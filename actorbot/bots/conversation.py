from actorbot.api import messaging
from actorbot.utils import logger


class Conversation(object):
    """
    Base conversation object.
    You need redefine message_handler, response_handler methods for build
    your own conversation.
    """

    slashCommands = (
        ('/help', 'show this message'))
    startText = '''
        Hi! I'm a bot!
        Type me [/help](send:/help) for more command.
    '''

    def __init__(self, owner, peer):
        """
        """
        self._owner = owner
        self._peer = peer
        self._id = 0
        self._sent = []
        logger.debug('[%s] start conversation: %s',
                     self._owner.name, self._peer.id)

    def _get_id(self):
        """
        Get next number for message
        """
        self._id += 1
        return '%d%05d' % (self._peer.id, self._id)

    async def message_handler(self, message):
        """
        Process messages from peer
        """
        if message.text == '/help':
            self.help(peer)
        if message.text == '/start':
            self.start(peer)

    def send(self, message):
        """
        Send any message
        """
        self._sent.append(message.id)
        self._owner.toSend(message)

    async def response_handler(self, message):
        """
        Process responses from server
        """
        self._sent.remove(message.id)
        logger.debug('[%s] confirmed (%d): %s',
                     self._owner.name, len(self._sent), message.id)

    def sendText(self, text):
        """
        Just send some text to peer
        """
        message = messaging.TextMessage(text=text)
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=self._peer,
                                        message=message)
        self.send(out_msg)

    def help(self):
        """
        Send help text
        """
        text = '\n'.join(['[/%s](send:/%s) - %s' % (c[0], c[0], c[1]) for c in self.slashCommands])
        self.sendText(text)

    def start(self):
        """
        Send start text
        """
        self.sendText(self.startText)
