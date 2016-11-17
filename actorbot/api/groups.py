from actorbot.api import MessageOut, Body, Services

from actorbot.utils import logger


class CreateGroup(MessageOut):
    def __init__(self, message_id, title):
        body = Body(body_type='CreateGroup',
                    title=title)
        super().__init__(message_id, Services.Groups, body)


class CreateGroupWithOwner(MessageOut):
    def __init__(self, message_id, title, owner, members):
        body = Body(body_type='CreateGroupWithOwner',
                    title=title,
                    user=owner, members=members)
        super().__init__(message_id, Services.Groups, body)


class UpdateShortName(MessageOut):
    def __init__(self, message_id, groupId, shortName):
        body = Body(body_type='UpdateGroupShortName',
                    groupId=groupId, shortName=shortName)
        super().__init__(message_id, Services.Groups, body)


class InviteUser(MessageOut):
    def __init__(self, message_id, groupPeer, userPeer):
        body = Body(body_type='InviteUser',
                    groupPeer=groupPeer, userPeer=userPeer)
        super().__init__(message_id, Services.Groups, body)


class AddGroupExtString(MessageOut):
    def __init__(self, message_id, groupId, key, value):
        body = Body(body_type='AddGroupExtString',
                    groupId=groupId, key=key, value=value)
        super().__init__(message_id, Services.Groups, body)


class AddGroupExtBool(MessageOut):
    def __init__(self, message_id, groupId, key, value):
        body = Body(body_type='AddGroupExtBool',
                    groupId=groupId, key=key, value=value)
        super().__init__(message_id, Services.Groups, body)


class RemoveExt(MessageOut):
    def __init__(self, message_id, groupId, key):
        body = Body(body_type='RemoveGroupExt',
                    groupId=groupId, key=key)
        super().__init__(message_id, Services.Groups, body)
