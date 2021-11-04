#   ©Xiler - Arthurdw

from datetime import datetime
from enum import Enum

codes = list(map(lambda i: f"\033[{i}m",
                 [0, 2, 4, 5, 7, 8, 21, 22, 24, 25, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45,
                  46, 47, 49, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 102, 103, 104, 105, 106, 107]))


class Formats(Enum):
    r"""
    Enum for console formats/styling codes.

    Example:
        print(f"{Formats.underline.value}Underline text{Formats.default.value}")

    NOTE
    --------
    Some CLI's may not support this formatting.
    """
    default = "\033[0m\033[21m\033[22m\033[24m\033[25m\033[27m\033[28m"
    dim = "\033[2m"
    underline = "\033[4m"
    blink = "\033[5m"
    inverted = "\033[7m"
    hidden = "\033[8m"


class Colors(Enum):
    r"""
    Enum for console color codes.

    Example:
        print(f"{Colors.yellow.value}Yellow text{Colors.default.value}")

    NOTE
    --------
    Some CLI's may not support colors.
    """
    default = "\033[39m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    light_gray = "\033[37m"
    dark_gray = "\033[90m"
    light_red = "\033[91m"
    light_green = "\033[92m"
    light_yellow = "\033[93m"
    light_blue = "\033[94m"
    light_magenta = "\033[95m"
    light_cyan = "\033[96m"
    white = "\033[97m"


class Backgrounds(Enum):
    r"""
    Enum for console background color codes.

    Example:
        print(f"{Backgrounds.red.value}This text has a red background{Backgrounds.default.value}")

    NOTE
    --------
    Some CLI's may not support background colors.
    """
    default = "\033[49m"
    black = "\033[40m"
    red = "\033[41m"
    green = "\033[42m"
    yellow = "\033[43m"
    blue = "\033[44m"
    magenta = "\033[45m"
    cyan = "\033[46m"
    light_gray = "\033[47m"
    dark_gray = "\033[100m"
    light_red = "\033[101m"
    light_green = "\033[102m"
    light_yellow = "\033[103m"
    light_blue = "\033[104m"
    light_magenta = "\033[105m"
    light_cyan = "\033[106m"
    white = "\033[107m"


class Prettier:
    r"""
    UtilsX its solution for easily formatting your consoles. Prettier
    can make your programs look more professional with almost no effort!

    Parameters
    ------------
    datetime_format: :class:`str`
        The datetime format that your entered datetime object will take.
        The default format is `[%y-%d-%m %H:%M:%S] `.
    default_text_format: :class:`str`
        The default way text will be formatted in a print. This can be a
        color, format or background. (or combined)
    colors_enabled: :class:`bool`
        If colors should be enabled in the console. If false it will strip
        all color codes from the message.
    auto_strip_message: :class:`bool`
        If the pretty printer should automatically apply the python .strip()
        method to the content.
    """

    def __init__(self, **kwargs):
        self.datetime_format = \
            str(kwargs.get("datetime_format") or
                f"{Formats.default.value + Colors.dark_gray.value + Backgrounds.default.value}["
                f"{Colors.light_green.value}%y-%d-%m %H:%M:%S{Colors.dark_gray.value}]{Colors.default.value} ")

        self.default_text_format = \
            str(kwargs.get("default_text_format") or Formats.default.value + Colors.default.value +
                Backgrounds.default.value)

        # 'x if x is not None else `default`' -> Cheat code to check if a x is passed and if its not None (undefined)
        self.colors_enabled = bool(kwargs.get("colors_enabled") if kwargs.get("colors_enabled") is not None else True)
        self.auto_strip_message = \
            bool(kwargs.get("auto_strip_message") if kwargs.get("auto_strip_message") is not None else False)

    @staticmethod
    def clear_colors(msg: str):
        r"""
        Clears all known color codes from a given message.

        Parameters
        ------------
        msg: :class:`str`
            The message that is the target.

        Returns
        ------------
        :class:`str`
            A color code stripped string.
        """
        for code in codes:
            msg = msg.replace(code, "")
        return msg

    def print(self, message: str, time: datetime = None) -> None:
        r"""
        Pretty prints a given message.

        Parameters
        ------------
        message: :class:`str`
            The message that must be pretty printed
        time: :class:`datetime`
            The printed datetime object. (Optional)
        """
        print(self.format(message, time))

    def format(self, message: str, time: datetime = None) -> str:
        r"""
        Formats a message, this method is also called in the
        Prettier print statement!

        Parameters
        ------------
        message: :class:`str`
            The message that must be formatted
        time: :class:`datetime`
            The printed datetime object. (Optional)

        Returns
        ------------
        :class:`str`
            A formatted string.
        """
        data = str((self.format_timestamp(time) if time is not None else '') + self.default_text_format +
                   (message.strip() if self.auto_strip_message else message))
        return data if self.colors_enabled else self.clear_colors(data)

    def format_timestamp(self, time: datetime) -> str:
        r"""
        Formats a datetime object, this method is also called in the
        Prettier format statement!

        Parameters
        ------------
        time: :class:`datetime`
            The datetime object that must be formatted

        Returns
        ------------
        :class:`str`
            A formatted datetime object.
        """
        formatted = time.strftime(self.datetime_format)
        return formatted if self.colors_enabled else self.clear_colors(formatted)
