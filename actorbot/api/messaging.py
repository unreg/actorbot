from actorbot.api import BaseMessage, MessageOut, Body, Services
from actorbot.api import random_id


class TextMessage(BaseMessage):
    def __init__(self, text, message_type='Text'):
        data = {
            'type': message_type,
            'text': text
        }
        super().__init__(data)


class DocumentMessage(BaseMessage):
    def __init__(self, fileId, accessHash, fileSize,
                 name, mimeType, thumb, ext, message_type="Document"):
        data = {
            'type': message_type,
            'fileId': fileId,
            'accessHash': accessHash,
            'fileSize': fileSize,
            'name': name,
            'mimeType': mimeType,
            'thumb': thumb,
            'ext': ext
        }
        super().__init__(data)


class SendMessage(MessageOut):
    def __init__(self, message_id, peer, message):
        body = Body(body_type='SendMessage',
                    randomId=random_id(message_id),
                    peer=peer, message=message)
        super().__init__(message_id, Services.Messaging, body)


class UpdateMessageContent(MessageOut):
    def __init__(self, message_id, peer, randomId, message):
        body = Body(body_type='UpdateMessageContent',
                    randomId=randomId,
                    peer=peer, updatedMessage=message)
        super().__init__(message_id, Services.Messaging, body)
