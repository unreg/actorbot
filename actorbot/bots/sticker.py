from actorbot.bots import Conversation


class StickerConv(Conversation):
    """
    """

    slashCommands = (
        ('createpack', 'create sticker pack'),
        ('selectpack', 'select sticker pack as current'),
        ('addsticker', 'create sticker in current pack'),
        ('delsticker', 'delete sticker from current pack'),
        ('showstickers', 'show stickers from current pack'),
        ('help', 'list commands'))

    def message_handler(self, message):
        """
        """
        super().message_handler(message)

        peer = message.body.peer
        message = message.body.message
        if message.type != 'Text':
            return
