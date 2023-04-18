import os
import sys
import json
import click
import requests
import subprocess
import pkg_resources
from pathlib import Path
from getpass import getpass
from clint.textui import progress

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out, authentication


PIF: Path = Path(Path(__file__).parent, 'install.json')
sys.argv[0] = sys.argv[0][:-3]


def find_prg(program: str) -> bool:
    """
    The task of this function is to find programs and return their path.

    :param program: Programs name in string format.
    :return: bool
    """

    bins: Path = Path(Path(__file__).parent.parent.parent.parent, 'krnl/bins/', program)

    stnd: Path = Path(Path(__file__).parent.parent, program)

    extn: Path = Path(Path(__file__).parent.parent.parent, 'extn/', program)

    return True if bins.exists() or stnd.exists() or extn.exists() else False


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


def read_pif(pif_url: str) -> dict:
    """
    This function reads the required information of each program from the PIF (Program Information File).

    :param pif_url: URL address of PIF.
    :return: dict
    """

    return json.loads(requests.get(pif_url).text)


def dl_file(url: str) -> bool:
    """
    The task of this function is to download the specified files.

    :param url: The URL address of the file to be downloaded.
    :return: bool
    """

    prg_type: str = Path(url).parent.parent.name

    match prg_type:
        case 'bins':
            dest: Path = Path(Path(__file__).parent.parent.parent.parent, 'krnl/bins/', Path(url).parent.name)
        case 'stnd':
            dest: Path = Path(Path(__file__).parent.parent, Path(url).parent.name)
        case 'extn':
            dest: Path = Path(Path(__file__).parent.parent.parent, 'extn/', Path(url).parent.name)
        case _:
            return False

    try:
        response: requests.Response = requests.get(url, stream=True)

        if not dest.exists():
            os.mkdir(dest)

        with open(Path(dest, Path(url).name), "wb") as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                      label=f'Downloading {Path(url).name}\t',
                                      expected_size=(total_length / 1024) + 1):
                if chunk:
                    file.write(chunk)
                    file.flush()

    except requests.RequestException:
        return False
    else:
        return True


def install_requirements(pif: dict) -> bool:
    """
    The task of this function is to download and install the required packages of each program.

    :param pif: PIF in dictionary.
    :return: bool
    """

    required: set = {pkg for pkg in pif['requirements']}

    installed: set = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if len(missing) > 0:
        msg_out(nature='standard', message='\nInstall the required packages...')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        except requests.RequestException:
            return False

    return True


def dl_plugins(pif_url: str) -> bool:
    """
    The task of this function is to download and install the required plugins of each program.

    :param pif_url: URL address of PIF.
    :return: bool
    """

    pif = read_pif(pif_url=pif_url)

    try:
        for pl in pif["plugins"]:
            response: requests.Response = requests.get(Path(Path(pif_url).parent, pl).__str__())

            if response.status_code == 200:
                dl_file(response.url)

    except requests.RequestException:
        return False
    else:
        return True


@click.command(help=get_description(PIF))
@click.option('--version', is_flag=True, help="Show version of this program.")
@click.option('-a', '--alone', is_flag=True, help="The program will be installed without installing the required packages.")
@click.argument('program', required=False)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if kwargs['program'] is None:
            msg_out(nature='standard',
                    message="Usage: install [OPTIONS] [PROGRAM]\nTry 'install --help' for help.\n\nError: Missing argument -> 'PROGRAM'.")
        else:
            auth_pass = getpass()
            if authentication(tkn_pass=auth_pass,
                              pass_file=Path(Path(__file__).parent.parent.parent.parent, 'setg/PASS.json')):

                if find_prg(program=kwargs['program']):
                    msg_out(nature='error', message=f"Error: The '{kwargs['program']}' program is already installed.")
                else:
                    srch_status, srch_response = search_in_repo(program=kwargs['program'])
                    if srch_status:
                        pif_repo: dict = read_pif(pif_url=srch_response)

                        success_msg: bool = False

                        if kwargs['alone']:

                            if dl_file(url='/'.join(srch_response.split('/')[:-1]) + f"/{pif_repo['executable']}") and \
                               dl_file(url=srch_response) and \
                               dl_plugins(pif_url=srch_response):

                                success_msg = True

                            if success_msg:
                                msg_out(nature='success',
                                        message=f"The '{kwargs['program']}' program has been successfully installed.")
                            else:
                                msg_out(nature='error', message="Unfortunately, the program was not installed correctly. Please try again.")
                        else:
                            install_status: bool = install_requirements(pif=pif_repo)

                            if install_status:
                                if dl_file(url='/'.join(srch_response.split('/')[:-1]) + f"/{pif_repo['executable']}") and \
                                   dl_file(url=srch_response) and \
                                   dl_plugins(pif_url=srch_response):

                                    success_msg = True

                                if success_msg:
                                    msg_out(nature='success',
                                            message=f"The '{kwargs['program']}' program has been successfully installed.")
                                else:
                                    msg_out(nature='error',
                                            message="Error: Unfortunately, the program was not installed correctly. Please try again.")
                            else:
                                msg_out(nature='error',
                                        message='Error: There is a connection problem that prevents the installation of packages.\nPlease check your internet connection.')
                    else:
                        msg_out(nature='error', message=srch_response)
            else:
                msg_out(nature='error', message='Error: Authentication failed!')


if __name__ == '__main__':
    main()