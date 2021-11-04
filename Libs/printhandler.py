from datetime import datetime

from utilsX.console import Prettier, Colors

d = Colors.default.value

r = Colors.red.value
lr = Colors.light_red.value

b = Colors.blue.value
lb = Colors.light_blue.value

y = Colors.yellow.value
ly = Colors.light_yellow.value


# Handles most console messages.
class PrintHandler:
    def __init__(self, prettier: Prettier, log: bool):
        self.log = log
        self.prettier = prettier
        self.info_prefix = f"\b{b}[{lb}INFO{b}]{d} "
        self.warning_prefix = f"\b{y}[{ly}WARN{y}]{d} "
        self.fatal_prefix = f"\b{r}[{lr}FATAL{r}]{d} "

    def printf(self, message: str) -> None:
        """
        Format prints a message to the console.
        (date + message)
        :param message: The message that must be printed.
        """
        self.prettier.print(message + d, datetime.now())

    def info(self, message: str) -> None:
        """
        Sends a message with the INFO prefix.
        :param message: The message that must be printed.
        """
        if self.log:
            self.printf(self.info_prefix + message)

    def warn(self, message: str) -> None:
        """
        Sends a message with the WARN prefix.
        :param message: The message that must be printed.
        """
        if self.log:
            self.printf(self.warning_prefix + message)

    def fatal(self, message: str) -> None:
        """
        Sends a message with the FATAL prefix.
        :param message: The message that must be printed.
        """
        if self.log:
            self.printf(self.fatal_prefix + message)