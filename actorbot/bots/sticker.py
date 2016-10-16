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
    admins = ['']

    def message_handler(self, message):
        """
        """
        peer = message.body.peer
        message = message.body.message

        if message.type != 'Text':
            return
        if message.text == '/help':
            self.help(peer)
        elif message.text == '/start':
            self.start(peer)
        elif self.admins and (peer.id not in self.admins):
            self.sendText(
                peer, text='Access denied. Administrator rights are required.')
            return
