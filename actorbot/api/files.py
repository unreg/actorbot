from actorbot.api import MessageOut, Services, Body

from actorbot.utils import logger


class DownloadFile(MessageOut):
    def __init__(self, message_id, fileLocation):
        body = Body(body_type='DownloadFile',
                    fileLocation=fileLocation)
        super().__init__(message_id, Services.Files, body)


class UploadFile(MessageOut):
    def __init__(self, message_id, bytes):
        body = Body(body_type='UploadFile',
                    bytes=bytes)
        super().__init__(message_id, Services.Files, body)
