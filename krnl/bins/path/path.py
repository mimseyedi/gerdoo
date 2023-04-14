import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF = Path(Path(__file__).parent, 'path.json')


def find_path(program: str) -> None:
    """
    This function does the main work of the 'path' program.
    The task of this function is to find the program path.

    :param program: Program name in string format.
    :return: None
    """

    bins: Path = Path(Path(__file__).parent.parent, program)

    stnd: Path = Path(Path(__file__).parent.parent.parent.parent, 'prgs/stnd/', program)

    extn: Path = Path(Path(__file__).parent.parent.parent.parent, 'prgs/extn/', program)

    response = bins if bins.exists() else (stnd if stnd.exists() else (extn if extn.exists() else False))

    if isinstance(response, Path):
        msg_out(nature='standard', message=response.__str__())
    else:
        msg_out(nature='error', message=f'Error: Program not found -> ({program})')


def path(command: list) -> None:
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
@click.argument('program_name', required=False)
def main(version, program_name):
    if version:
        get_version(PIF)
    else:
        if program_name is None:
            msg_out(nature='standard',
                    message="Usage: path [OPTIONS] [PROGRAM_NAME]\nTry 'path --help' for help.\n\nError: Missing argument -> 'PROGRAM_NAME'.")
        else:
            find_path(program=program_name)