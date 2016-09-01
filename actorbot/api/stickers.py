from actorbot.api import MessageOut, Services, Body

from actorbot.utils import logger


class CreateStickerPack(MessageOut):
    def __init__(self, message_id, creatorUserId):
        body = Body(body_type='CreateStickerPack',
                    creatorUserId=creatorUserId)
        super().__init__(message_id, Services.Stickers, body)


class AddSticker(MessageOut):
    def __init__(self, message_id, ownerUserId, packId, emoji,
                 small, smallW, smallH, medium, mediumW, mediumH,
                 large, largeW, largeH):
        body = Body(body_type='AddSticker',
                    ownerUserId=ownerUserId, packId=packId, emoji=emoji,
                    small=small, smallW=smallW, smallH=smallH,
                    medium=medium, mediumW=mediumW, mediumH=mediumH,
                    large=large, largeW=largeW, largeH=largeH)
        super().__init__(message_id, Services.Stickers, body)


class MakeStickerPackDefault(MessageOut):
    def __init__(self, message_id, userId, packId):
        body = Body(body_type='MakeStickerPackDefault',
                    userId=userId, packId=packId)
        super().__init__(message_id, Services.Stickers, body)


class ShowStickers(MessageOut):
    def __init__(self, message_id, ownerUserId, packId):
        body = Body(body_type='ShowStickers',
                    ownerUserId=ownerUserId, packId=packId)
        super().__init__(message_id, Services.Stickers, body)


class DeleteSticker(MessageOut):
    def __init__(self, message_id, ownerUserId, packId, stickerId):
        body = Body(body_type='DeleteSticker',
                    ownerUserId=ownerUserId, packId=packId,
                    stickerId=stickerId)
        super().__init__(message_id, Services.Stickers, body)
