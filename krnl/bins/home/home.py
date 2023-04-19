import os
import sys
import json
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF = Path(Path(__file__).parent, 'home.json')


def goto_home(where_opt: bool= False) -> str|None:
    """
    This function does the main work of the 'home' program.
    The task of this function is to change the working directory to the home directory.

    :param where_opt: It means that the (-w, --where) option is selected.
    :return: str|None
    """

    path_file_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PATH.json')

    if path_file_path.exists() and len(path_file_path.read_text()) > 0:
        with open(path_file_path, 'r') as path:
            try:
                home_path = json.load(path)['home']

                if where_opt:
                    if isinstance(home_path, str):
                        return home_path

                os.chdir(home_path)

            except KeyError:
                msg_out(nature='error', message='Error: PATH file is broken!')

            except json.JSONDecodeError:
                msg_out(nature='error', message='Error: PATH file is broken!')

            except FileNotFoundError:
                msg_out(nature='error', message=f'Error: The home path does not exist -> ({home_path})')

            except NotADirectoryError:
                msg_out(nature='error', message=f'Error: The home path is not a directory path -> ({home_path})')
    else:
        msg_out(nature='error', message=f'Error: The PATH file does not exist: \n{path_file_path}')


def home(command: list) -> None:
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
@click.option("--version", is_flag=True, help='Show the version of this program.')
@click.option("-w", "--where", is_flag=True, help='The home directory path will be displayed.')
def main(version, where):
    if version:
        get_version(PIF)
    elif where:
        response = goto_home(where_opt=True)
        if isinstance(response, str):
            msg_out(nature='standard', message=response)
    else:
        goto_home()
