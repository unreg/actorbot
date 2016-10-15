from actorbot.utils import logger


class Conversation(object):
    """
    """
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
        return '%d%05d'% (self._uid, self._id)

    def message_handler(self, message):
        """
        """
        pass

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
