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

    def __init__(self, owner, uid):
        """
        """
        self._owner = owner
        self._uid = uid
        self._id = 0
        self._sent = []
        logger.debug('[%s] start conversation: %s',
                     self._owner.name, self._uid)

    def _get_id(self):
        """
        """
        self._id += 1
        return '%d%05d' % (self._uid, self._id)

    def message_handler(self, message):
        """
        """
        peer = message.body.peer
        message = message.body.message

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

    def sendText(self, peer, text):
        """
        """
        message = messaging.TextMessage(text=text)
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=peer,
                                        message=message)
        self.send(out_msg)

    def help(self, peer):
        """
        """
        text = '\n'.join(['[/%s](send:/%s) - %s' % (c[0], c[0], c[1]) for c in self.slashCommands])
        self.sendText(peer, text)

    def start(self, peer):
        """
        """
        self.sendText(peer, self.startText)
