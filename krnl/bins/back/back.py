import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version


PIF: Path = Path(Path(__file__).parent, 'back.json')


def go_back() -> None:
    """
    This function does the main work of the 'back' program.
    It means moving the user to the previous directory of the current directory.

    :return: None
    """

    os.chdir("..")


def back(command: list) -> None:
    """
    This function is the bridge between the kernel and the task and interface of this program.

    :param command: User command in the form of a list.
    :return: None
    """

    sys.argv = command
    try:
        main()
    except SystemExit:
        pass


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(version):
    get_version(PIF) if version else go_back()
