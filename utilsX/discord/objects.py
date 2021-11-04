from typing import Union

from nextcord import Color


class Embed:
    r"""
    The embed object that UtilsX can process.

    Attributes
    -----------
    color: :class:`Union[Color, int]`
            The color of the embed bar.
    title: :class:`str`
            The title for the embed.
    image: :class:`str`
        The url for a image that will be set as the embed image.
    thumbnail: :class:`str`
        The url for a image that will be set as the embed thumbnail.
    """
    def __init__(self, *, color: Union[Color, int] = None, title: str = None, image: str = None, thumbnail: str = None):
        self.title = title
        self.color = color
        self.image = image
        self.thumbnail = thumbnail


class Footer:
    r"""
    The footer object that UtilsX can process.

    Attributes
    -----------
    text: :class:`str`
        The text that will be visible in the footer.
    icon_url: :class:`str`
        An image url for the footer icon.
    timestamp: :class:`bool`
        If a timestamp should be visible.
    """
    def __init__(self, text: str = "", icon_url: str = "", timestamp: bool = False):
        self.text = text
        self.icon_url = icon_url
        self.timestamp = timestamp


class Author:
    r"""
    The author object that UtilsX can process.

    Attributes
    -----------
    name: :class:`Union[Color, int]`
        The text that will be in the author name field.
    url: :class:`str`
        The url to what the author section should link.
    icon_url: :class:`bool`
        An image url for the author icon.
    """
    def __init__(self, name: str, url: str = "", icon_url: str = ""):
        self.name = name
        self.url = url
        self.icon_url = icon_url


class Field:
    r"""
    The field object that UtilsX can process.

    Attributes
    -----------
    name: :class:`Union[Color, int]`
        The title for the field.
    value: :class:`str`
        The main content for the field.
    inline: :class:`bool`
        If the field should be inline.
    """
    def __init__(self, name: str, value: str, inline: bool = False):
        self.name = name
        self.value = value
        self.inline = inline
