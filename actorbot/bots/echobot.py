from actorbot.bots import Conversation
from actorbot.api import messaging


class EchoConversation(Conversation):
    """
        Simple echo bot
    """
    async def message_handler(self, message):
        """ """
        out_msg = messaging.SendMessage(self._get_id(),
                                        peer=self._peer,
                                        message=message)
        self.send(out_msg)

    async def response_handler(self, message):
        """ """
        await super().response_handler(message)
