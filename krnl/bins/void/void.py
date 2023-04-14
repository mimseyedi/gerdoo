import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version


PIF = Path(Path(__file__).parent, 'void.json')


def void(command: list) -> None:
    """
    This function is the bridge between the kernel and the task and interface of this program.

    :param command: User command in the form of a list.
    :return: None
    """

    sys.argv = command

    if len(sys.argv) == 1:
        main(standalone_mode=True)
    else:
        try:
            main()
        except SystemExit:
            pass


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(version):
    if version:
        get_version(PIF)
    else:
        return True
