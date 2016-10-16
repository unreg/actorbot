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
    admins = []
    command = ''
    stage = 0

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
        elif message.text == '/createpack':
            self.createpack(peer, message)
        else:
            if self.command == 'createpack':
                self.createpack(peer, message)

    def createpack(self, peer, message):
        """
        """
        if self.command and (self.command != 'createpack'):
            self.sendText(peer, 'Wrong command')
            return
        if self.stage == 0:
            self.stage = 1
            self.command = 'createpack'
            self.sendText(peer, text='Enter name for you new stickerpack')
            return
        if self.stage == 1:
            self.stage = 2
            text = 'You enter: %s' % message.text
            self.sendText(peer, text=text)
            return