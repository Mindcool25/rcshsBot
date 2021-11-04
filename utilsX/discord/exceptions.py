class UtilsXDiscordException(Exception):
    """The base exception for the UtilsX discord section!"""
    pass


class MissingFormatArguments(UtilsXDiscordException):
    """Exception that gets thrown when a `.format` raises an error due to missing keys."""
    pass
