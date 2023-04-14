import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF = Path(Path(__file__).parent, 'bash.json')


def execute_bash_cmd(command: list) -> None:
    """
    This function does the main work of the 'bash' program.
    The work of this function is to execute bash commands.

    :param command: Bash command in the form of a list.
    :return: None
    """

    os.system(' '.join(command))


def bash(command: list) -> None:
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
@click.argument('bash_command', required=False, nargs=-1)
def main(version, bash_command):
    if version:
        get_version(PIF)
    else:
        if len(bash_command) == 0:
            msg_out(nature='standard',
                    message="Usage: bash [OPTIONS] [BASH_COMMAND]..\nTry 'bash --help' for help.\n\nError: Missing argument -> 'BASH_COMMAND'.")
        else:
            execute_bash_cmd(command=bash_command)