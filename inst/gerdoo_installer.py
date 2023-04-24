"""
                    _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

gerdoo_installer

This program can install gerdoo to the system along with
the latest changes and information in the repository.

For more information: https://github.com/mimseyedi/gerdoo#gerdoo_installer
"""


import sys
import urllib.error
from urllib import request
try:
    request.urlopen('http://google.com', timeout=3)
except urllib.error.URLError:
    print("\033[91mError: No internet connection.\033[0m")
    sys.exit()

import os
import json
import hashlib
import subprocess
import pkg_resources
from pathlib import Path
try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
    import requests

try:
    from clint.textui import progress
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "clint"], stdout=subprocess.DEVNULL)
    from clint.textui import progress

try:
    import prompt_toolkit
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.completion import PathCompleter

    if prompt_toolkit.__version__ != "3.0.38":
        raise ImportError()

except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.38"], stdout=subprocess.DEVNULL)
    import prompt_toolkit
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.completion import PathCompleter


def read_repo(url: str) -> dict:
    """
    This function reads the required installation information from the repository.

    :param url: The installation information url address.
    :return: dict
    """

    return json.loads(requests.get(url).text)


def install_requirements(install_info: dict) -> bool:
    """
    This function installs the required packages.

    :param install_info: The installation information dict.
    :return: bool
    """

    required: set = {pkg for pkg in install_info['packages']}

    installed: set = {pkg.key for pkg in pkg_resources.working_set}

    missing = required - installed

    if len(missing) > 0:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        except requests.RequestException:
            return False

    return True


def initializing(root_path: Path) -> None:
    """
    This function is responsible for the initial setup and creates directories and paths.

    :param root_path: The root or main path of installation dir.
    :return: None
    """

    directories: list = ['krnl',
                         Path('krnl', 'bins').__str__(),
                         'shll',
                         'mdls',
                         'setg',
                         'prgs',
                         Path('prgs', 'stnd').__str__(),
                         Path('prgs', 'extn').__str__(),
                         'updt',
                         'vrsn']

    os.chdir(root_path)

    for dirc in directories:
        os.mkdir(dirc)


def get_path(root_path: Path, directory: str) -> Path:
    """
    This function returns the correct paths according to the selected directory.

    :param root_path: The root or main path of installation dir.
    :param directory: Directory name.
    :return:
    """

    match directory:
        case 'main':
            return Path(root_path)
        case 'krnl':
            return Path(root_path, 'krnl')
        case 'shll':
            return Path(root_path, 'shll')
        case 'mdls':
            return Path(root_path, 'mdls')
        case 'bins':
            return Path(root_path, 'krnl', 'bins')
        case 'stnd':
            return Path(root_path, 'prgs', 'stnd')
        case 'updt':
            return Path(root_path, 'updt')
        case 'vrsn':
            return Path(root_path, 'vrsn')


def create_setg_files(root_path: Path, PASS: dict, PATH: dict) -> None:
    """
    The task of this function is to create configuration files.

    :param root_path: The root or main path of installation dir.
    :param PASS: User passwords information in dict.
    :param PATH: User paths information in dict.
    :return: None
    """

    with open(Path(root_path, 'setg', 'PASS.json'), 'w') as PASS_file:
        json.dump(PASS, PASS_file)

    with open(Path(root_path, 'setg', 'PATH.json'), 'w') as PATH_file:
        json.dump(PATH, PATH_file)


def hashing_password(password: str) -> str:
    """
    The task of this function is to hashing the user password.

    :param password: User password in str.
    :return: str
    """

    algorithm = hashlib.sha256()
    algorithm.update(password.encode("utf-8"))
    return algorithm.hexdigest()


def dl_file(url: str, dest: Path) -> bool:
    """
    The task of this function is to download the specified files.

    :param url: The URL address of the file to be downloaded.
    :param dest: Install destination.
    :return: bool
    """

    try:
        response: requests.Response = requests.get(url, stream=True)

        prg_name: str = Path(url).name
        space: str = " " * (((os.get_terminal_size()[0] // 2) + (len(prg_name) - 52) // 2) - len(prg_name))

        if dest.name == 'bins':
            dest = Path(dest, prg_name.split('.')[0])
            if not dest.exists():
                os.mkdir(dest)

        elif dest.name == 'stnd':
            dest = Path(dest, prg_name.split('.')[0])
            if not dest.exists():
                os.mkdir(dest)

        with open(Path(dest, Path(url).name), "wb") as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                      label=f'{space}{prg_name}\t' if len(prg_name) < 15 else f'{space}{prg_name}',
                                      expected_size=(total_length / 1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()

    except requests.RequestException:
        return False
    else:
        return True


def path_validation(path: str) -> str:
    """
    The task of this function is to validate the path.

    :param path: Path of directory.
    :return: str
    """

    if len(path) > 0 and path not in ['.', '..', '/', '\\']:
        if len(path) != path.count('/'):
            _path = Path(os.getcwd(), path)
            if _path.exists() and _path.is_dir():
                return _path.__str__()


def password_validation(conf_pass: str) -> str:
    """
    The task of this function is to validate password.

    :param conf_pass: The password confirmed.
    :return: str
    """

    if conf_pass == user_pass:
        return conf_pass


def reset_screen() -> None:
    """
    The task of this function is to clear the screen and print the installation header.

    :return: None
    """

    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

    logo = ["                    _",
            "                   | |",
            "  __ _  ___ _ __ __| | ___   ___",
            " / _` |/ _ \ '__/ _` |/ _ \ / _ \\",
            "| (_| |  __/ | | (_| | (_) | (_) |",
            " \__, |\___|_|  \__,_|\___/ \___/",
            "  __/ |",
            " |___/"]

    for line in logo:
        space = " " * ((os.get_terminal_size()[0] - 40) // 2)
        print(space, line)

    print("\n\n")


def print_in_middle(message: str) -> None:
    """
    The task of this function is to print message in the middle of the screen.

    :param message: Anything in str format.
    :return: None
    """

    half_line = os.get_terminal_size()[0] // 2
    space = " " * ((half_line + len(message) // 2) - len(message))
    print(space + message)


def main() -> None:
    """
    Main function -> Start point.

    :return: None
    """

    try:
        reset_screen()
        print("Please specify the installation path:\n")

        path_validator = Validator.from_callable(
            path_validation,
            error_message='The selected path must already exist and also be a directory!',
            move_cursor_to_end=True)

        install_path = prompt_toolkit.prompt("[1] Installation path -> ", validator=path_validator,
                                             validate_while_typing=False, completer=PathCompleter())


        if Path(install_path, "gerdoo").exists() and Path(install_path, "gerdoo").is_dir():
            reset_screen()
            print_in_middle("\033[91mError: A directory named gerdoo already exists in this path\033[0m")
        else:
            os.mkdir(Path(install_path, 'gerdoo'))
            install_path = Path(install_path, 'gerdoo')

            reset_screen()
            print("Please enter your home address::\n")

            home_path = prompt_toolkit.prompt("[2] The home path -> ", validator=path_validator,
                                              validate_while_typing=False, completer=PathCompleter())

            reset_screen()
            print("Please choose your password:\n")

            global user_pass

            user_pass = prompt_toolkit.prompt("[3] The password -> ", is_password=True)

            pass_validator = Validator.from_callable(
                password_validation,
                error_message='Passwords are not the same!',
                move_cursor_to_end=True)

            reset_screen()
            print("Please confirm your password:\n")

            confirm_pass = prompt_toolkit.prompt("[4] The password -> ", validator=pass_validator,
                                                 validate_while_typing=True, is_password=True)


            hashed_pass: str = hashing_password(password=confirm_pass)

            reset_screen()

            print_in_middle("Installing the required packages ...")

            install_info: dict = read_repo(url="https://raw.githubusercontent.com/mimseyedi/gerdoo/master/inst/inst_map.json")

            if install_requirements(install_info=install_info):

                reset_screen()
                print_in_middle("Building program directories...")

                initializing(root_path=Path(install_path))

                reset_screen()
                print_in_middle("Download and install programs from the repository...\n")

                programs: list = ['main', 'krnl', 'shll', 'mdls', 'bins', 'stnd', 'updt', 'vrsn']

                for program in programs:
                    for file in install_info[program]:
                        if not dl_file(url=file, dest=get_path(root_path=Path(install_path), directory=program)):
                            reset_screen()
                            print_in_middle("\033[91mError: The installation process was interrupted due to a problem in the connection to the Internet.\033[0m")
                            print_in_middle("Please try again.")
                            sys.exit()

                create_setg_files(root_path=Path(install_path),
                                 PASS={"user_pass": hashed_pass},
                                 PATH={"home": home_path})

                print()
                print_in_middle("\033[92mgerdoo has been successfully installed.\033[0m")

            else:
                sys.exit()

    except KeyboardInterrupt:
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
        sys.exit()


if __name__ == '__main__':
    main()