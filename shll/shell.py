"""
                     _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

shell

shell is the first program that runs.
shell is a CLI program that is placed between the user and the kernel
to send user commands to the kernel and finally display the output to the user.

For more information: https://github.com/mimseyedi/gerdoo#shell
"""


import os
import sys
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import ANSI, HTML
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.completion import Completer, Completion

sys.path.append(Path(__file__).parent.parent.__str__())
import krnl.kernel as kernel


class ItemsInCurrentDirCompleter(Completer):
    """
    Customized Completer class to display a dropdown of items in the
    current directory with details such as item type, size, etc.
    """

    @staticmethod
    def get_items(dir_path: str | Path) -> int:
        """
        This function return number of items (FILE/DIRS) in a directory.

        :param dir_path: Path of a directory in string or pathlib.Path format.
        :return: int
        """

        return len([item for item in os.listdir(dir_path) if not item.startswith('.')])


    @staticmethod
    def get_size(byte: int) -> str:
        """
        A function to calculate and then display the size of the item in an optimal state.

        :param byte: Item size in bytes.
        :return: int
        """

        for rng in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if byte < 1024.0:
                return "%3.0f %s" % (byte, rng)
            byte /= 1024.0


    def get_completions(self, document, complete_event) -> Completion:
        """
        An overridden method to display the completer of items in a directory.

        :param document: :class:`~prompt_toolkit.document.Document` instance.
        :param complete_event: :class:`.CompleteEvent` instance.
        :return: Completion
        """

        items: list = [item for item in os.listdir(os.getcwd()) if not item.startswith('.')]

        meta_dict: dict = {}

        for item in items:
            item_path: Path = Path(os.getcwd(), item)

            if item_path.is_dir():
                meta_dict[item] = HTML(
                    f"<style bg='#C0C0C0' color='#008000'>Type(Directory) - {self.get_size(os.path.getsize(item_path))} - {self.get_items(item_path)} items</style>")
            else:
                meta_dict[item] = HTML(
                    f"<style bg='#C0C0C0' color='#008000'>Type(File) - {self.get_size(os.path.getsize(item_path))}</style>")

        word = document.get_word_before_cursor()

        for item in items:
            if item.startswith(word):
                yield Completion(item, start_position=-len(word),
                                 display=item, display_meta=meta_dict.get(item), )


def main() -> None:
    """
    The starting point of the program.

    :return: None
    """

    # Clear the screen:
    kernel.execute(program='clear')
    # Go to home directory:
    kernel.execute(program='home')

    season = PromptSession(history=InMemoryHistory())

    while True:
        command = season.prompt(ANSI(f'\033[32m➜ \033[36;1m{Path(os.getcwd()).name}:\033[0m '),
                                completer=ItemsInCurrentDirCompleter(),
                                complete_style=CompleteStyle.MULTI_COLUMN).lstrip().split()

        if len(command) > 0:
            kernel.execute(program=command[0], args=command[1:])


if __name__ == '__main__':
    main()
