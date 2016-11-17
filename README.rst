========
ActorBot
========

A simple python implementation `Actor Messaging <https://github.com/actorapp>`_ bot API
======================================================

Features
========

* simple, small and extensible. It's easy to write own `Actor Messaging <https://github.com/actorapp>`_ bots.
* pure Python with asyncio and aiohttp
* websocket connection to Actor ws|wss API-endpoint
* sending and receiving messages
* API module
* `LICENSE <https://github.com/unreg/actorbot/blob/master/LICENSE.txt>`_

API module
==========

- Messaging: SendMessage, UpdateMessageContent

- Groups: CreateGroup, CreateGroupWithOwner, UpdateShortName, AddGroupExtString, AddGroupExtBool, RemoveExt, InviteUser

- KeyValue: SetVAlue, GetValue, DeleteValue, GetKeys

- Files: UploadFile, DownloadFile

- Stickers: CreateStickerPack, AddSticker, ShowStickerPacks, ShowStickers, DeleteSticker, MakeStickerPackDefault, UnmakeStickerPackDefault,

- Bots: CreateBot

- Users: FindUser, ChangeUserName, ChangeUserNickname, ChangeUserAbout, ChangeUserAvatar, IsAdmin, AddSlashCommand, RemoveSlashCommand, AddUserExtString, AddUserExtBool, RemoveUserExt


Requirements
============

* Python >= 3.5.1
* `aiohttp >= 0.22.0 <https://github.com/KeepSafe/aiohttp>`_
* async_timeout >= 1.1.0 (optional)


Getting started
===============


Make your own conversation inherited from base class *Conversation*. For example simple echo bot (more in `Wiki <https://github.com/unreg/actorbot/wiki>`_):

.. code-block:: python

    from actorbot.bots import Conversation
    from actorbot.api import messaging


    class EchoConversation(Conversation):
        """ Simple echo bot """
        async def message_handler(self, message):
            out_msg = messaging.SendMessage(self._get_id(),
                                            peer=self._peer,
                                            message=message)
            await self.send(out_msg)

        async def response_handler(self, message):
            await super().response_handler(message)


run one or more bots through starter:

.. code-block:: python

    from actorbot import Bot
    from actorbot.bots import EchoConversation

    ...

    ownbot = Bot(endpoint='YOUR_ACTOR_SERVER_ENDPOINT',
                 token='YOUR_BOT_TOKEN',
                 name='SOME_BOT_NAME',
                 conversation=EchoConversation)

    bots = [ownbot]

    transports = [asyncio.ensure_future(bot.transport.run()) for bot in bots]
    processors = [asyncio.ensure_future(bot.run()) for bot in bots]

    loop.run_until_complete(asyncio.wait(transports + processors))

    ...

Feedback
--------

Join in Actor group https://actor.im/join/pyactorbot
