from datetime import datetime
from typing import List, Union

from nextcord import Embed, File, AllowedMentions, Color
from nextcord.abc import Messageable
from nextcord.ext import commands
from nextcord.message import Message

from . import objects as obj
from .handlers import MessageHandler, FooterHandler, AuthorHandler, EmbedHandler


class Cog(commands.Cog):
    r"""
    The commands.Cog implemented Cog object. This
    processes the bot COG object.

    Attributes
    -----------
    message_handler: :class:`MessageHandler`
        The message handler object.
    embed_handler: :class:`EmbedHandler`
        The default embed object.
    footer_handler: :class:`FooterHandler`
        The footer handler object.
    author_handler: :class:`AuthorHandler`
        The author handler object.
    """

    def __init__(self):
        self.message_handler = MessageHandler()
        self.embed_handler = EmbedHandler(obj.Embed())
        self.footer_handler = FooterHandler(obj.Footer())
        self.author_handler = AuthorHandler(obj.Author(""))

    def handle_message(self, message: str, format_args: dict, handler_enabled: bool) -> str:
        """
        Handles all messages using the set message handler object.

        Parameters
        -----------
        message: :class:`str`
            The message that should get processed.
        format_args: :class:`dict`
            The format arguments that will be implemented in the prefix and suffix.
        handler_enabled: :class:`bool`
            If the message should get handled using the set message handler object.
        """
        if format_args is None:
            format_args = {}
        return self.message_handler.process(message, **format_args) \
            if self.message_handler and handler_enabled else message

    async def send(self, target: Messageable, message: str, *, tts: bool = False, embed: Embed = None,
                   file: File = None, files: List[File] = None, nonce: int = None, delete_after: float = None,
                   allowed_mentions: AllowedMentions = None, handler_enabled: bool = True, format_args: dict = None
                   ) -> Message:
        """
        Processes a message and forwards it to the default nextcord.py send method.

        Parameters
        -----------
        target: :class:`Messageable`
            The location where the message should get sent to.
        message: :class:`str`
            The message that should get processed.
        tts: :class:`bool`
            If TTS should be enabled for the message.
        embed: :class:`Embed`
            A nextcord.py embed object for sending embeds the old classical way.
        file: :class:`File`
            A nextcord.py file that will be sent in the message.
        files: :class:`List[File]`
            A list of nextcord.py files that will all be sent in the message.
        nonce: :class:`int`
            The nonce repl value.
        delete_after: :class:`float`
            The amount of seconds the message should be visible.
        allowed_mentions: :class:`AllowedMentions`
            An nextcord.py AllowedMentions object.
        handler_enabled: :class:`bool`
            If the message should get handled using the set message handler object.
        format_args: :class:`dict`
            The format arguments that will be implemented in the prefix and suffix.


        Returns
        ------------
        Message
            A sent nextcord.py message.
        """
        message = self.handle_message(message, format_args, handler_enabled)
        return await target.send(message, tts=tts, embed=embed, file=file, files=files, nonce=nonce,
                                 delete_after=delete_after, allowed_mentions=allowed_mentions)

    async def embed(self, target: Messageable, message: str, *, title: str = None, raw: str = "",
                    handler_enabled: bool = True, color: Union[Color, int] = None, format_args: dict = None,
                    image: str = None, thumbnail: str = None, footer: obj.Footer = None, author: obj.Author = None,
                    fields: List[obj.Field] = None, get_embed: bool = False) -> Union[Message, Embed]:
        """
        Processes a message and forwards it to the default nextcord.py send method.

        Parameters
        -----------
        target: :class:`Messageable`
            The location where the message should get sent to.
        message: :class:`str`
            The message that should get processed.
        title: :class:`str`
            The title for the embed.
        raw: :class:`str`
            The non embedded content.
        handler_enabled: :class:`bool`
            If the message should get handled using the set message handler object.
        color: :class:`Union[Color, int]`
            The color of the embed bar.
        format_args: :class:`dict`
            The format arguments that will be implemented in the prefix and suffix.
        image: :class:`str`
            The url for a image that will be set as the embed image.
        thumbnail: :class:`str`
            The url for a image that will be set as the embed thumbnail.
        footer: :class:`obj.Footer`
            A UtilsX footer object that will format the embed footer section.
        author: :class:`obj.Author`
            A utilsX author object that will format the embed author section.
        fields: :class:`List[obj.Field]`
            A list (up to 25) objects that will format the embed fields.
        get_embed: :class:`bool`
            If this boolean is set to true it will return the generated embed object. Default is false.


        Returns
        ------------
        Message
            A sent nextcord.py message.
        """
        message = self.handle_message(message, format_args, handler_enabled)
        embed_data = self.embed_handler.process(
            obj.Embed(color=color, title=title or " ", image=image, thumbnail=thumbnail))
        embed = Embed(title=embed_data.title, color=embed_data.color, description=message)
        if embed_data.image:
            embed.set_image(url=embed_data.image)
        if embed_data.thumbnail:
            embed.set_thumbnail(url=embed_data.thumbnail)
        footer = self.footer_handler.process(footer)
        if footer:
            embed.set_footer(text=footer.text, icon_url=footer.icon_url)
            if footer.timestamp:
                embed.timestamp = datetime.now()
        author = self.author_handler.process(author)
        if author:
            embed.set_author(name=author.name, url=author.url, icon_url=author.icon_url)
        if fields:
            for field in fields:
                embed.add_field(name=field.name, value=field.value, inline=field.inline)
        if get_embed:
            return embed
        return await target.send(raw, embed=embed)
