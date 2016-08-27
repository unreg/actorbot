from actorbot.api import MessageOut, Services, Body
from actorbot.api import random_id

from actorbot.utils import logger


class SetValue(MessageOut):
    def __init__(self, message_id, keyspace, key, value):
        body = Body(body_type='SetValue',
                    keyspace=keyspace, key=key, value=value)
        super().__init__(message_id, Services.KeyValue, body)


class GetValue(MessageOut):
    def __init__(self, message_id, keyspace, key):
        body = Body(body_type='GetValue',
                    keyspace=keyspace, key=key)
        super().__init__(message_id, Services.KeyValue, body)


class DeleteValue(MessageOut):
    def __init__(self, message_id, keyspace, key):
        body = Body(body_type='DeleteValue',
                    keyspace=keyspace, key=key)
        super().__init__(message_id, Services.KeyValue, body)


class GetKeys(MessageOut):
    def __init__(self, message_id, keyspace):
        body = Body(body_type='GetKeys',
                    keyspace=keyspace)
        super().__init__(message_id, Services.KeyValue, body)
