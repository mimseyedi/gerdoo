import sys
import json
import click
from pathlib import Path
from getpass import getpass

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out, authentication, str_to_sha256


PIF: Path = Path(Path(__file__).parent, 'setg.json')


def change_password(new_pass: str) -> None:
    """
    This function can change the user password.

    :param new_pass: New user password in str form.
    :return: None
    """

    PASS_file_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PASS.json')

    if PASS_file_path.exists():
        try:
            with open(PASS_file_path, 'r') as read_PASS:
                PASS_info: dict = json.load(read_PASS)

            PASS_info['user_pass'] = str_to_sha256(new_pass)

            with open(PASS_file_path, 'w') as write_PASS:
                json.dump(PASS_info, write_PASS)

            msg_out(nature='success', message="Password changed successfully.")

        except json.JSONDecodeError:
            msg_out(nature='error', message='Error: The PASS file is corrupted.')
        except KeyError:
            msg_out(nature='error', message='Error: The PASS file is corrupted.')
    else:
        msg_out(nature='error', message='Error: There is no PASS file!')


def change_home_path(new_home_path: Path) -> None:
    """
    This function can change the home path.

    :param new_home_path: New home path in pathlib.Path form.
    :return: None
    """

    PATH_file_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PATH.json')

    if PATH_file_path.exists():
        if new_home_path.exists() and new_home_path.is_dir():
            try:
                with open(PATH_file_path, 'r') as read_PATH:
                    PATH_info: dict = json.load(read_PATH)

                PATH_info['home'] = new_home_path.__str__()

                with open(PATH_file_path, 'w') as write_PATH:
                    json.dump(PATH_info, write_PATH)

                msg_out(nature='success', message="The home path changed successfully.")

            except json.JSONDecodeError:
                msg_out(nature='error', message='Error: The PATH file is corrupted.')
            except KeyError:
                msg_out(nature='error', message='Error: The PATH file is corrupted.')
        else:
            msg_out(nature='error', message='Error: The home path must be a directory and exist.')
    else:
        msg_out(nature='error', message='Error: There is no PATH file!')


@click.group(help=get_description(PIF), invoke_without_command=True)
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(sys.argv) == 1:
            msg_out(nature='standard',
                    message="Usage: setg [OPTIONS]\nTry 'setg --help' for help.\n\nError: Missing commands.")


@main.command(help="This command changes the home path.")
@click.argument("path", nargs=1)
def chpath(path):
    auth_pass = getpass()
    if authentication(tkn_pass=auth_pass,
                      pass_file=Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PASS.json')):

        change_home_path(new_home_path=Path(path))
    else:
        msg_out(nature='error', message='Error: Authentication failed!')


@main.command(help="This command changes the user password.")
@click.argument("password", nargs=1)
def chpass(password):
    auth_pass = getpass()
    if authentication(tkn_pass=auth_pass,
                      pass_file=Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PASS.json')):

        change_password(new_pass=password)
    else:
        msg_out(nature='error', message='Error: Authentication failed!')


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()
