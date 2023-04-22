"""
                    _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

gerdoo_updater

This program can update the main programs if there are any changes by
coordinating between the installed files and the repository.

For more information: https://github.com/mimseyedi/gerdoo#gerdoo_updater
"""


import sys
import json
import requests
import urllib.error
from urllib import request
from pathlib import Path
from clint.textui import progress
from prompt_toolkit.shortcuts import confirm


def read_repo(url: str) -> bool|dict:
    """
    This function reads the required update information from the repository.

    :param url: The update information url address.
    :return: bool|dict
    """

    try:
        return json.loads(requests.get(url).text)
    except json.JSONDecodeError:
        return False
    except requests.RequestException:
        return False


def read_updt_map_or_any_pif(path: Path) -> bool|dict:
    """
    The task of this function is to read update map or any PIF.

    :param path: Path of PIF or update map in .json.
    :return: bool|dict
    """

    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return False
    except FileNotFoundError:
        return False


def is_update(sys_updt_map: dict, repo_updt_map: dict) -> bool:
    """
    The task of this function is to check for updates.

    :param sys_updt_map: System update map.
    :param repo_updt_map: Repository update map.
    :return: bool
    """

    return True if sys_updt_map != repo_updt_map else False


def dl_file(url: str, dest: Path) -> bool:
    """
    The task of this function is to download the specified files.

    :param url: The URL address of the file to be downloaded.
    :param dest: update destination.
    :return: bool
    """

    try:
        response: requests.Response = requests.get(url, stream=True)

        prg_name: str = Path(url).name

        with open(Path(dest, Path(url).name), "wb") as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.mill(response.iter_content(chunk_size=1024),
                                      label=f'Updating {prg_name}\t',
                                      expected_size=(total_length / 1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()

    except requests.RequestException:
        return False

    return True


def update(updt_map: dict) -> None:
    """
    The task of this function is to update the main programs.

    :param updt_map: Repository update map in dict.
    :return: None
    """

    dl_file(url="https://raw.githubusercontent.com/mimseyedi/gerdoo/master/updt/updt_map.json",
           dest=Path(Path(__file__).parent, 'updt_map.json'))

    MAIN_PROGRAM: dict = {'krnl': Path(Path(__file__).parent.parent, 'krnl', 'kernel.json'),
                          'shll': Path(Path(__file__).parent.parent, 'shll', 'shell.json'),
                          'mdls': Path(Path(__file__).parent.parent, 'mdls', 'gerdoolib.json')}

    for program, info in updt_map.items():
        pif: dict = read_updt_map_or_any_pif(path=MAIN_PROGRAM[program])

        if isinstance(pif, dict):
            repo_version: str = info[0]
            syst_version: str = pif["version"]

            if repo_version != syst_version:
                for url in info[1:]:
                    dl_file(url=url, dest=MAIN_PROGRAM[program].parent)

        else:
            print("\033[91mError: A problem prevented the update. Please repair first and then try again.\033[0m")
            return


def main():
    """
    Main function -> Start point.

    :return: None
    """

    repo_updt: bool|dict = read_repo(url="https://raw.githubusercontent.com/mimseyedi/gerdoo/master/updt/updt_map.json")

    if isinstance(repo_updt, dict):
        syst_updt: bool|dict = read_updt_map_or_any_pif(path=Path(Path(__file__).parent, 'updt_map.json'))

        if isinstance(syst_updt, dict):
            is_updt: bool = is_update(sys_updt_map=syst_updt, repo_updt_map=repo_updt)

            if is_updt:
                ask_to_updt: bool = confirm("There is an update for gerdoo. Do you want to update?")

                if ask_to_updt:
                    try:
                        request.urlopen('http://google.com', timeout=3)
                    except urllib.error.URLError:
                        print("\033[91mError: No internet connection.\033[91m\nYou must be connected to the Internet to update gerdoo.\033[0m")
                        sys.exit()
                    else:
                        update(updt_map=repo_updt)
                else:
                    sys.exit()
            else:
                sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()


if __name__ == '__main__':
    main()