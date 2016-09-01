from actorbot.api import MessageOut, Services, Body

from actorbot.utils import logger


class FindUser(MessageOut):
    def __init__(self, message_id, query):
        body = Body(body_type='FindUser',
                    query=query)
        super().__init__(message_id, Services.Users, body)


class ChangeUserName(MessageOut):
    def __init__(self, message_id, userId, name):
        body = Body(body_type='ChangeUserName',
                    userId=userId, name=name)
        super().__init__(message_id, Services.Users, body)


class ChangeUserNickname(MessageOut):
    def __init__(self, message_id, userId, nickname):
        body = Body(body_type='ChangeUserNickname',
                    userId=userId, nickname=nickname)
        super().__init__(message_id, Services.Users, body)


class ChangeUserAbout(MessageOut):
    def __init__(self, message_id, userId, about):
        body = Body(body_type='ChangeUserAbout',
                    userId=userId, about=about)
        super().__init__(message_id, Services.Users, body)


class ChangeUserAvatar(MessageOut):
    def __init__(self, message_id, userId, fileLocation):
        body = Body(body_type='ChangeUserAvatar',
                    userId=userId, fileLocation=fileLocation)
        super().__init__(message_id, Services.Users, body)


class IsAdmin(MessageOut):
    def __init__(self, message_id, userId):
        body = Body(body_type='IsAdmin', userId=userId)
        super().__init__(message_id, Services.Users, body)


class AddSlashCommand(MessageOut):
    def __init__(self, message_id, userId, command):
        body = Body(body_type='AddSlashCommand',
            userId=userId, command=command)
        super().__init__(message_id, Services.Users, body)


class RemoveSlashCommand(MessageOut):
    def __init__(self, message_id, userId, command):
        body = Body(body_type='RemoveSlashCommand',
            userId=userId, command=command)
        super().__init__(message_id, Services.Users, body)


class AddUserExtString(MessageOut):
    def __init__(self, message_id, userId, key, value):
        body = Body(body_type='AddUserExtString',
            userId=userId, key=key, value=value)
        super().__init__(message_id, Services.Users, body)


class AddUserExtBool(MessageOut):
    def __init__(self, message_id, userId, key, value):
        body = Body(body_type='AddUserExtBool',
            userId=userId, key=key, value=value)
        super().__init__(message_id, Services.Users, body)


class RemoveUserExt(MessageOut):
    def __init__(self, message_id, userId, key):
        body = Body(body_type='RemoveUserExt',
            userId=userId, key=key)
        super().__init__(message_id, Services.Users, body)
