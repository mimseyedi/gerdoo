import os
import sys
import json
import click
import requests
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'repo.json')


def read_pif(mode: str, address: str|Path) -> bool|dict:
    """
    Reading the file containing program information is done by this function.

    :param mode: 'file' or 'url'
    :param address: PIF path on system or PIF url in repo.
    :return: bool|dict
    """

    if mode == 'file':
        address: Path = Path(address) if isinstance(address, str) else address

        return json.loads(address.read_text(encoding='utf-8')) if address.exists() and \
               len(address.read_text()) > 0 else False

    elif mode == 'url':
        try:
            return json.loads(requests.get(address).text)
        except requests.RequestException:
            return False

    else:
        raise ValueError("The mode argument must between ['file', 'url'].")


def get_programs() -> dict:
    """
    This function returns all programs installed on the system
    along with their versions in the form of a dictionary.

    :return: dict
    """

    bins: Path = Path(Path(__file__).parent.parent.parent.parent, 'krnl', 'bins')

    stnd: Path = Path(Path(__file__).parent.parent)

    extn: Path = Path(Path(__file__).parent.parent.parent, 'extn')

    paths, programs = [bins, stnd, extn], {}

    for path in paths:
        for prg in os.listdir(path):
            prg_pif: Path = Path(path, prg, f'{prg}.json')
            if prg_pif.exists():
                pif: dict = read_pif(mode='file', address=prg_pif)
                programs[prg] = pif['version']

    return programs


def search_in_repo(program: str) -> tuple[bool, str]:
    """
    The task of this function is to find programs in the repository.

    :param program: Programs name in string format.
    :return: tuple[bool, str]
    """

    bins_repo: str = "https://github.com/mimseyedi/gerdoo/tree/master/krnl/bins/" + program

    stnd_repo: str = "https://github.com/mimseyedi/gerdoo/tree/master/prgs/stnd/" + program

    extn_repo: str = "https://github.com/mimseyedi/gerdoo/tree/master/prgs/extn/" + program

    prg_type: int = -1

    for typ, url in enumerate([bins_repo, stnd_repo, extn_repo]):
        try:
            response: int = requests.get(url=url).status_code
            if response == 200:
                prg_type = typ
        except requests.RequestException:
            return False, f"Error: There is a connection problem. Please check your internet connection."

    match prg_type:
        case 0:
            return True, f"https://raw.githubusercontent.com/mimseyedi/gerdoo/master/krnl/bins/{program}/{program}.json"
        case 1:
            return True, f"https://raw.githubusercontent.com/mimseyedi/gerdoo/master/prgs/stnd/{program}/{program}.json"
        case 2:
            return True, f"https://raw.githubusercontent.com/mimseyedi/gerdoo/master/prgs/extn/{program}/{program}.json"

    if prg_type == -1:
        return False, f"Error: Program '{program}' was not found in the repository."

    return False, f"Error: There is a connection problem. Please check your internet connection."


def describe(programs: dict, pif: dict) -> None:
    """
    Describes a program in the repository relative to its status on the system.

    :param programs: All programs on system.
    :param pif: Program Information File in dict form.
    :return: None
    """

    if pif['name'] in programs.keys():
        if pif['version'] != programs[pif['name']]:
            status: str = 'Updatable'
        else:
            status: str = 'Installed'
    else:
        status: str = 'Not installed'

    msg_out(nature='standard',
            message=f'Name: {pif["name"]}\nVersion: {pif["version"]}\nDescription: {pif["description"]}\nStatus: {status}')


def get_updatables(programs: dict) -> None:
    """
    This function shows the programs that can be updated.

    :param programs: All programs on system.
    :return: None
    """

    updatables: dict = {}

    for prg in programs.keys():
        status, response = search_in_repo(program=prg)

        if status:
            pif: dict = read_pif(mode='url', address=response)

            if programs[prg] != pif['version']:
                updatables[prg] = pif['version']
        else:
            if response.endswith('connection.'):
                msg_out(nature='error', message=response)
                break
            else:
                continue

    if len(updatables) > 0:
        msg_out(nature='standard',
                message='PROGRAM\tSYSTEM\tREPO')

        for prg in updatables:
            msg_out(nature='standard',
                    message=f'{prg}\t{programs[prg]}\t{updatables[prg]}')
    else:
        msg_out(nature='success',
                message='All programs are up to date!')


def get_new_programs(programs: dict) -> None:
    """
    This function shows the new programs that are not installed on the system.

    :param programs: All programs on system.
    :return: None
    """

    try:
        bins_response: requests.Response = requests.get("https://github.com/mimseyedi/gerdoo/tree/master/krnl/bins")

        stnd_response: requests.Response = requests.get("https://github.com/mimseyedi/gerdoo/tree/master/prgs/stnd")

        extn_response: requests.Response = requests.get("https://github.com/mimseyedi/gerdoo/tree/master/prgs/extn")

        new_programs: list = []

        for dirs in [bins_response, stnd_response, extn_response]:
            soup = BeautifulSoup(dirs.text, "html.parser")
            items = soup.findAll("a", class_="js-navigation-open Link--primary")

            prgs: list = [item.text.strip() for item in items]

            new_prgs: list = [prg for prg in prgs if prg not in programs.keys()]

            new_programs.extend(new_prgs)

        if len(new_programs) > 0:
            msg_out(nature='standard',
                    message='PROGRAM\t\tDESCRIPTION')

            for prg in new_programs:
                status, response = search_in_repo(prg)
                if status:
                    pif: dict = read_pif(mode='url', address=response)
                    msg_out(nature='standard',
                            message=f"{prg}\t\t{pif['description'][:55]}{'...' if len(pif['description']) > 55 else ''}")

        else:
            msg_out(nature='success',
                    message='All programs are already installed on your system.')

    except requests.RequestException:
        msg_out(nature='error',
                message="Error: There is a connection problem. Please check your internet connection.")


def get_installed_programs(programs: dict) -> None:
    """
    This function will show all the programs installed on system.

    :param programs: All programs on system.
    :return: None
    """

    msg_out(nature='standard', message='PROGRAM\t\t\tVERSION')

    max_length: int = max([len(program) for program in programs.keys()])
    SPACE_TO_VERSION: int = 25

    for program, version in programs.items():
        space = " " * abs(SPACE_TO_VERSION - len(program))
        msg_out(nature='standard', message=f'{program}{space}{version}')


@click.command(help=get_description(PIF))
@click.option('--version', is_flag=True, help="Show version of this program.")
@click.option('-u', '--updatables', is_flag=True, help="Show programs that can be updated.")
@click.option('-p', '--programs', is_flag=True, help="Show new programs that are not installed on your system.")
@click.option('-i', '--installed', is_flag=True, help="Show all programs installed on system.")
@click.option('-s', '--search', help="Search for programs in the repository.")
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(sys.argv) == 1:
            msg_out(nature='standard',
                    message="Usage: repo [OPTIONS]\nTry 'repo --help' for help.\n\nError: Missing options.")

        elif kwargs['updatables']:
            programs: dict = get_programs()
            get_updatables(programs=programs)

        elif kwargs['programs']:
            programs: dict = get_programs()
            get_new_programs(programs=programs)

        elif kwargs['installed']:
            programs: dict = get_programs()
            get_installed_programs(programs=programs)

        elif kwargs['search'] is not None:
            programs: dict = get_programs()
            status, response = search_in_repo(kwargs['search'])
            if status:
                pif: dict = read_pif(mode='url', address=response)

                describe(programs=programs, pif=pif)
            else:
                msg_out(nature='error', message=response)


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()