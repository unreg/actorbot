import asyncio

from actorbot import ActorBot
from actorbot.api import messaging

from actorbot.utils import logger


class EchoBot(ActorBot):
    """
    """
    async def _delivered(self, response):
        """
        """
        logger.debug('[%s] message id=%s delivered: %s',
                     self._name, response.id, response.body.date)

    async def message_handler(self, message):
        await super().message_handler(message)
        peer = message.body.peer
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=peer,
                                        message=message.body.message)
        self.send(out_msg, callback=self._delivered)
