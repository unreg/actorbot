from actorbot.bots import Conversation
from actorbot.api import messaging

from actorbot.utils import logger


class EchoConv(Conversation):
    """
    """
    def message_handler(self, message):
        """
        """
        peer = message.body.peer
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=peer,
                                        message=message.body.message)
        self.send(out_msg)
