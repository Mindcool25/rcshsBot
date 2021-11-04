from random import randint
from typing import Union

from nextcord import Color

from .exceptions import MissingFormatArguments
from .objects import Footer, Author, Embed


class MessageHandler:
    r"""
    The object that handles all messages that are sent through the Cog object.

    Parameters
    ------------
    prefix: :class:`str`
        The string that will be prepended.
    suffix: :class:`str`
        The string that will be appended.
    """

    def __init__(self, *, prefix: str = "", suffix: str = ""):
        self.prefix = prefix
        self.suffix = suffix

    def process(self, message: str, **kwargs) -> str:
        r"""
        Message processor for the MessageHandler.

        Parameters
        ------------
        message: :class:`str`
            The message that will be processed.
        **kwargs:
            The formatting for the message.

        Returns
        ------------
        :class:`str`
            A formatted string.

        Raises
        ------------
        MissingFormatArguments
            If not all format parameters have been filled.
        """
        try:
            return self.prefix.format(**kwargs) + message + self.suffix.format(**kwargs)
        except KeyError as e:
            args = ', '.join([f"'{arg}'" for arg in e.args])
            raise MissingFormatArguments(f"Missing format arguments {args}. "
                                         f"(fix eg, `format_args={{'{e.args[0]}': 'Cool String'}}`)")


class FooterHandler:
    r"""
    The object that handles embed footers.

    Parameters
    ------------
    footer: :class:`Footer`
        The default footer object.
    """

    def __init__(self, footer: Footer):
        self.footer = footer

    def process(self, obj: Union[Footer, None]) -> Union[Footer, None]:
        r"""
        Handles the embed footers.

        Parameters
        ------------
        obj: :class:`Union[Footer, None]`
            The new provided footer.

        Returns
        ------------
        :class:`Union[Footer, None]`
            A valid footer object or None
        """
        if obj:
            return Footer(text=(obj.text or self.footer.text),
                          icon_url=(obj.icon_url or self.footer.icon_url),
                          timestamp=(obj.timestamp if obj.timestamp else self.footer.timestamp))
        elif self.footer:
            return self.footer
        return None


class AuthorHandler:
    r"""
    The object that handles the embed author field.

    Parameters
    ------------
    author: :class:`Author`
        The default author object.
    """

    def __init__(self, author: Author):
        self.author = author

    def process(self, obj: Union[Author, None]) -> Union[Author, None]:
        r"""
        Handles the embed author property.

        Parameters
        ------------
        obj: :class:`Union[Author, None]`
            The new provided author.

        Returns
        ------------
        :class:`Union[Author, None]`
            A valid author object or None
        """
        if obj:
            return Author(name=obj.name,
                          url=(obj.url or self.author.url),
                          icon_url=(obj.icon_url or self.author.icon_url))
        elif self.author:
            return self.author
        return None


class EmbedHandler:
    r"""
    The object that handles the general embed structure.

    Parameters
    ------------
    embed: :class:`Embed`
        The default author object.
    """

    def __init__(self, embed: Embed):
        self.embed = embed

    def process(self, obj: Union[Embed, None]) -> Union[Embed, None]:
        r"""
        Handles the general embed object.

        Parameters
        ------------
        obj: :class:`Union[Embed, None]`
            The new provided Embed.

        Returns
        ------------
        :class:`Union[Author, None]`
            A valid embed object or None
        """
        if obj:
            return Embed(color=(obj.color or self.embed.color or Color(int(hex(randint(0, 16581375)), 0))),
                         title=(obj.title or self.embed.title),
                         image=(obj.image or self.embed.image),
                         thumbnail=(obj.thumbnail or self.embed.thumbnail))
        elif self.embed:
            return self.embed
        return None
