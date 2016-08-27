from actorbot.api import MessageOut, Body, Services

from actorbot.utils import logger


class CreateGroup(MessageOut):
    def __init__(self, message_id, title):
        body = Body(body_type='CreateGroup',
                    title=title)
        super().__init__(message_id, Services.Groups, body)


class InviteUser(MessageOut):
    def __init__(self, message_id, groupPeer, userPeer):
        body = Body(body_type='InviteUser',
                    groupPeer=groupPeer, userPeer=userPeer)
        super().__init__(message_id, Services.Groups, body)
