from actorbot.api import BaseMessage, MessageOut, Body, Services
from actorbot.api import random_id

from actorbot.utils import logger


class TextMessage(BaseMessage):
    def __init__(self, text, message_type='Text'):
        data = {
            'type': message_type,
            'text': text
        }
        super().__init__(data)


class SendMessage(MessageOut):
    def __init__(self, message_id, peer, message):
        body = Body(body_type='SendMessage',
                    randomId=random_id(message_id),
                    peer=peer, message=message)
        super().__init__(message_id, Services.Messaging, body)
