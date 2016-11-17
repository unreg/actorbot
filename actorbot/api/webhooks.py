from actorbot.api import MessageOut, Body, Services


class RegisterHook(MessageOut):
    def __init__(self, message_id, name):
        body = Body(body_type='RegisterHook', name=name)
        super().__init__(message_id, Services.WebHooks, body)


class GetHooks(MessageOut):
    def __init__(self, message_id):
        body = Body(body_type='GetHooks')
        super().__init__(message_id, Services.WebHooks, body)
