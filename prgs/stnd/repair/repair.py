import os
import sys
import json
import click
import requests
from pathlib import Path
from getpass import getpass
from clint.textui import progress

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out, authentication


PIF: Path = Path(Path(__file__).parent, 'repair.json')


def read_repo(url: str) -> dict:
    """
    This function is responsible for reading the PIFs in the repository.

    :param url: PIF url
    :return: dict
    """

    return json.loads(requests.get(url).text)


def scan_dir_and_files(dir_: Path, files: list, install_info: dict) -> tuple[dict, int]:
    """
    The task of this function is to scan program directories and files and find their errors.

    :param dir_: The directory path.
    :param files: Files in the directory in list form.
    :param install_info: Installation information dict.
    :return: tuple[dict, int]
    """

    errors: int = 0
    problems: dict = {}

    if dir_.exists():
        msg_out(nature='standard', message=f"\033[92m+EXISTS\033[0m\t{dir_}")
        for file in files:
            if file in os.listdir(dir_):
                msg_out(nature='standard', message=f"\033[92m+EXISTS\033[0m\t{Path(dir_, file)}")

                for key, value in install_info.items():
                    for url in value:
                        if url.endswith(f"/{Path(file).name}"):
                            try:
                                response: requests.Response = requests.get(url)

                                with open(Path(dir_, file), 'r') as sys_file:
                                    if sys_file.read() == response.text:
                                        msg_out(nature='standard', message=f"\033[92m+INTACT\033[0m\t{Path(dir_, file)}")
                                    else:
                                        msg_out(nature='error', message=f"\033[91m-BROKEN\033[0m\t{Path(dir_, file)}")
                                        problems[Path(file).name.__str__().split('.')[0]] = set()
                                        problems[Path(file).name.__str__().split('.')[0]].add(Path(dir_, file).__str__())
                                        errors += 1

                            except requests.RequestException:
                                msg_out(nature='error', message='Error: No internet connection.')
                                break

            else:
                msg_out(nature='error', message=f"\033[91m-MISSED\033[0m\t{Path(dir_, file)}")
                problems[Path(file).name.__str__().split('.')[0]] = set()
                problems[Path(file).name.__str__().split('.')[0]].add(Path(dir_, file).__str__())
                errors += 1

    else:
        msg_out(nature='standard', message=f"\033[91m-MISSED\033[0m\t{dir_}")
        problems[dir_.name] = {dir_.__str__()}
        errors += 1

        for file in files:
            msg_out(nature='error', message=f"\033[91m-MISSED\033[0m\t{Path(dir_, file)}")
            problems[dir_.name].add(Path(dir_, file).__str__())
            errors += 1

    return problems, errors


def scan_log() -> bool|tuple[dict, int]:
    """
    This function reports scanned items.

    :return: bool|tuple[dict, int]
    """

    root_path: Path = Path(__file__).parent.parent.parent.parent

    dirs_and_files: dict = {root_path: ['gerdoo.py'],

                            Path(root_path, 'inst'): ['gerdoo_installer.py'],

                            Path(root_path, 'krnl'): ['kernel.py'],
                            Path(root_path, 'krnl', 'bins'): [],
                            Path(root_path, 'krnl', 'bins', 'back'): ['back.py', 'back.json'],
                            Path(root_path, 'krnl', 'bins', 'bash'): ['bash.py', 'bash.json'],
                            Path(root_path, 'krnl', 'bins', 'goto'): ['goto.py', 'goto.json'],
                            Path(root_path, 'krnl', 'bins', 'home'): ['home.py', 'home.json'],
                            Path(root_path, 'krnl', 'bins', 'path'): ['path.py', 'path.json'],
                            Path(root_path, 'krnl', 'bins', 'void'): ['void.py', 'void.json'],

                            Path(root_path, 'mdls'): ['__init__.py', 'gerdoolib.py'],

                            Path(root_path, 'prgs', 'extn'): [],

                            Path(root_path, 'prgs', 'stnd'): [],
                            Path(root_path, 'prgs', 'stnd', 'clear'): ['clear.py', 'clear.json'],
                            Path(root_path, 'prgs', 'stnd', 'deldir'): ['deldir.py', 'deldir.json'],
                            Path(root_path, 'prgs', 'stnd', 'delf'): ['delf.py', 'delf.json'],
                            Path(root_path, 'prgs', 'stnd', 'install'): ['install.py', 'install.json'],
                            Path(root_path, 'prgs', 'stnd', 'items'): ['items.py', 'items.json'],
                            Path(root_path, 'prgs', 'stnd', 'map'): ['map.py', 'map.json'],
                            Path(root_path, 'prgs', 'stnd', 'newdir'): ['newdir.py', 'newdir.json'],
                            Path(root_path, 'prgs', 'stnd', 'newf'): ['newf.py', 'newf.json'],
                            Path(root_path, 'prgs', 'stnd', 'repair'): ['repair.py', 'repair.json'],
                            Path(root_path, 'prgs', 'stnd', 'repo'): ['repo.py', 'repo.json'],
                            Path(root_path, 'prgs', 'stnd', 'setg'): ['setg.py', 'setg.json'],
                            Path(root_path, 'prgs', 'stnd', 'system'): ['system.py', 'system.json'],
                            Path(root_path, 'prgs', 'stnd', 'uninstall'): ['uninstall.py', 'uninstall.json'],
                            Path(root_path, 'prgs', 'stnd', 'update'): ['update.py', 'update.json'],

                            Path(root_path, 'setg'): ['PASS.json', 'PATH.json'],

                            Path(root_path, 'shll'): ['shell.py'],

                            Path(root_path, 'vrsn'): ['version.json'], }

    errors: int = 0
    problems: dict = {}

    install_info: dict = read_repo(url="https://raw.githubusercontent.com/mimseyedi/gerdoo/master/inst/inst_map.json")

    for key, value in dirs_and_files.items():
        response, error_count = scan_dir_and_files(dir_=key, files=value, install_info=install_info)
        errors += error_count
        problems = {**problems, **response}

    return (problems, errors) if len(problems) > 0 else False


def fix_dirs() -> bool|dict:
    """
    This function corrects related errors in the directory structure.

    :return: bool|dict
    """

    response = scan_log()

    if isinstance(response, tuple):
        msg_out(nature='error', message=f"\nMESSAGE: {response[1]} errors were found!")
        msg_out(nature='error', message="MESSAGE: Use the fix command to fix problems.")

        problems: dict = response[0]

        for key, value in problems.items():
            for path in value:
                if Path(path).suffix == '':
                    os.mkdir(path)

        return problems
    else:
        msg_out(nature='success', message='\nMESSAGE: there is no problem. Everything is in its place.')
        return False


def dl_file(url: str, dest: Path) -> None:
    """
    The task of this function is to download the required files.

    :param url: The url path of file in repository
    :param dest: The destination path.
    :return: None
    """

    try:
        response: requests.Response = requests.get(url, stream=True)

        prg_name: str = Path(url).name

        with open(Path(dest), "wb") as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                      label=f'Installing {prg_name}\t',
                                      expected_size=(total_length / 1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()

    except requests.RequestException:
        msg_out(nature='error', message='Error: No internet connection!')
        return


def fix_files(problems: dict, install_info: dict) -> None:
    """
    The task of this function is to remove and reinstall damaged files.

    :param problems: All problems with details in dict form.
    :param install_info: Installation information dict.
    :return: None
    """

    for key, value in install_info.items():
        if key in ['version', 'packages']:
            continue

        if key in problems.keys() and key not in ['bins', 'stnd']:
            for file in problems[key]:
                if Path(file).name == Path(value[0]).name:
                    dl_file(url=value[0], dest=file)
        else:
            for url in value:
                try:
                    for file in problems[Path(url).name.__str__().split('.')[0]]:
                        if Path(url).name == Path(file).name:
                            dl_file(url=url, dest=file)

                except KeyError:
                    pass


@click.group(help=get_description(PIF), invoke_without_command=True)
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(sys.argv) == 1:
            msg_out(nature='standard',
                    message="Usage: repair [OPTIONS] COMMAND [ARGS]...\nTry 'repair --help' for help.\n\nError: Missing command.")


@main.command(help="Problems are identified and then displayed.")
def scan():
    response = scan_log()

    if isinstance(response, tuple):
        msg_out(nature='error', message=f"\nMESSAGE: {response[1]} errors were found!")
        msg_out(nature='error', message="MESSAGE: Use the fix command to fix problems.")
    else:
        msg_out(nature='success', message='\nMESSAGE: there is no problem. Everything is in its place.')


@main.command(help="Identified problems are solved by connecting to the repository.")
def fix():
    auth_pass = getpass()
    if authentication(tkn_pass=auth_pass,
                      pass_file=Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PASS.json')):

        install_info: dict = read_repo(url="https://raw.githubusercontent.com/mimseyedi/gerdoo/master/inst/inst_map.json")

        problems: bool|dict = fix_dirs()

        if isinstance(problems, dict):
            msg_out(nature='standard', message='\nInstalling programs...\n')
            fix_files(problems=problems, install_info=install_info)


if __name__ == '__main__':
    main()
