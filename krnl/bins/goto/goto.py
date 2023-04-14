import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF = Path(Path(__file__).parent, 'goto.json')


def change_dir(dest: str) -> None:
    """
    This function does the main work of the 'goto' program.
    The task of this function is to move the user to the selected directory.

    :param dest: The directory selected as the destination.
    :return: None
    """

    try:
        os.chdir(dest)

    except FileNotFoundError:
        msg_out(nature='error', message=f'Error: The specified path does not exist -> ({dest})')

    except NotADirectoryError:
        msg_out(nature='error', message=f'Error: The specified path is not a directory path -> ({dest})')


def goto(command: list) -> None:
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
@click.option('--version', is_flag=True, help='Show version of this program.')
@click.argument('directory', required=False)
def main(version, directory):
    if version:
        get_version(PIF)
    else:
        if directory is None:
            msg_out(nature='standard',
                    message="Usage: goto [OPTIONS] [DIRECTORY]\nTry 'goto --help' for help.\n\nError: Missing argument -> 'DIRECTORY'.")
        else:
            change_dir(directory)