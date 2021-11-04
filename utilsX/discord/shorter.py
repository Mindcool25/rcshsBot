from typing import List, Iterable

from nextcord import Intents
from nextcord.ext import commands
from nextcord.ext.commands import Cog


class BotX(commands.Bot):
    r"""
    Shortens the code to create a bot instance.

    Parameters
    ----------
    intent: :class:`nextcord.Intents`
        The nextcord intents object that will be applied to the bot.

    Attributes
    -----------
    prefix: :class:`Union[str, callable, List[str]]`
        The bot its prefix, default is '!'
    description: :class:`str`
        The bot its description.
    case_insensitive: :class:`bool`
        If the bot will reply to all commands or only the
        case correct commands, default is True. (replies to all)
    intent: :class:`nextcord.Intents`
        The nextcord intents object that will be applied to the bot.
    """

    def __init__(self, intents=Intents()):
        self.prefix = "!"
        self.description = "Bot description is unset!\n" \
                           "Create a description by adding a `self.description = \"Your description\"` in the BotX init"
        self.case_insensitive = True
        self.intent = intents

        super().__init__(command_prefix=self.get_default_prefix, description=self.get_description(),
                         help_attrs=dict(hidden=True), case_insensitive=self.get_case_insensitive(),
                         intents=self.intent)

    def get_case_insensitive(self) -> bool:
        r"""
        Retrieves if the bot its case_insensitive status.
        """
        return self.case_insensitive

    def get_description(self) -> str:
        r"""
        Retrieves the bot description.
        """
        return self.description

    def get_default_prefix(self, *args, **kwargs) -> str:
        r"""
        Retrieves the bot prefix.
        """
        if callable(self.prefix):
            return self.prefix(*args, **kwargs)
        return self.prefix

    def run(self, token: str) -> None:
        r"""
        Runs the bot instance.

        Parameters
        -----------
        token: :class:`str`
            The bot its secret token.
        """
        super().run(token, reconnect=True)

    def load_extensions(self, extensions: List[str]) -> Iterable:
        r"""
        Loads all extensions from a list

        Parameters
        -----------
        extensions: :class:`List[str]`
            A list of extensions.
        """
        for extension in extensions:
            self.load_extension(extension)
            yield

    def unload_extensions(self, extensions: List[str]) -> Iterable:
        r"""
        Unloads all extensions from a list

        Parameters
        -----------
        extensions: :class:`List[str]`
            A list of extensions.
        """
        for extension in extensions:
            self.unload_extension(extension)
            yield

    def load_cogs(self, cogs: List[Cog]) -> None:
        r"""
        Loads all extensions from a list

        Parameters
        -----------
        cogs: :class:`List[Cogs]`
            A list of cogs.
        """
        for cog in cogs:
            self.add_cog(cog)

    def unload_cogs(self, cogs: List[str]) -> None:
        r"""
        Unloads all extensions from a list

        Parameters
        -----------
        cogs: :class:`List[str]`
            A list of cogs names.
        """
        for cog in cogs:
            self.remove_cog(cog)
