from actorbot.api import MessageOut, Services, Body

from actorbot.utils import logger


class CreateBot(MessageOut):
    def __init__(self, message_id, username, name):
        body = Body(body_type='CreateBot',
                    username=username, name=name)
        super().__init__(message_id, Services.Bots, body)
