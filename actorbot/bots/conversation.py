from actorbot.api import messaging
from actorbot.utils import logger


class Conversation(object):
    """
    """

    slashCommands = (
        ('/help', 'show this message'))
    startText = '''
        Hi! I'm a bot for stickers control.
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
        """
        self._id += 1
        return '%d%05d' % (self._peer.id, self._id)

    def message_handler(self, message):
        """
        """
        if message.text == '/help':
            self.help(peer)
        if message.text == '/start':
            self.start(peer)

    def send(self, message):
        """
        """
        self._sent.append(message.id)
        self._owner.toSend(message)

    def response_handler(self, message):
        """
        """
        self._sent.remove(message.id)
        logger.debug('[%s] confirmed (%d): %s',
                     self._owner.name, len(self._sent), message.id)

    def sendText(self, text):
        """
        """
        message = messaging.TextMessage(text=text)
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=self._peer,
                                        message=message)
        self.send(out_msg)

    def help(self):
        """
        """
        text = '\n'.join(['[/%s](send:/%s) - %s' % (c[0], c[0], c[1]) for c in self.slashCommands])
        self.sendText(text)

    def start(self):
        """
        """
        self.sendText(self.startText)
