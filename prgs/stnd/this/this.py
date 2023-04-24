import sys
import json
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'this.json')


def read_pif(pif_path: str|Path) -> bool|dict:
    """
    Reading the file containing program information is done by this function.

    :param pif_path: PIF path on system.
    :return: bool|dict
    """

    pif_path: Path = Path(pif_path) if isinstance(pif_path, str) else pif_path

    return json.loads(pif_path.read_text(encoding='utf-8')) if pif_path.exists() and \
           len(pif_path.read_text()) > 0 else False


def get_info(what: str='gerdoo') -> None:
    """
    This function returns information related to the specified main program.

    :param what: What information? ['gerdoo', 'kernel', 'shell', 'module']?
    :return: None
    """

    match what:
        case 'gerdoo':
            version_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'vrsn', 'version.json')

            install_path: Path = Path(Path(__file__).parent.parent.parent.parent)

            version_pif: bool|dict = read_pif(pif_path=version_path)

            if isinstance(version_pif, dict):
                msg_out(nature='standard', message=f'gerdoo version: {version_pif["version"]}')
            else:
                msg_out(nature='error', message='Error: The file related to gerdoo version information was not found.')

            msg_out(nature='standard', message=f"root path: {install_path.__str__()}")

        case 'kernel':
            kernel_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'krnl', 'kernel.json')

            kernel_pif: dict = read_pif(pif_path=kernel_path)

            if isinstance(kernel_pif, dict):
                msg_out(nature='standard', message=f'kernel version: {kernel_pif["version"]}')
                msg_out(nature='standard', message=f'kernel path: {kernel_path.parent.__str__()}')
            else:
                msg_out(nature='error', message='Error: The file related to kernel information was not found.')

        case 'shell':
            shell_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'shll', 'shell.json')

            shell_pif: dict = read_pif(pif_path=shell_path)

            if isinstance(shell_pif, dict):
                msg_out(nature='standard', message=f'shell version: {shell_pif["version"]}')
                msg_out(nature='standard', message=f'shell path: {shell_path.parent.__str__()}')
            else:
                msg_out(nature='error', message='Error: The file related to shell information was not found.')

        case 'module':
            module_path: Path = Path(Path(__file__).parent.parent.parent.parent, 'mdls', 'gerdoolib.json')

            module_pif: dict = read_pif(pif_path=module_path)

            if isinstance(module_pif, dict):
                msg_out(nature='standard', message=f'module version: {module_pif["version"]}')
                msg_out(nature='standard', message=f'module path: {module_path.parent.__str__()}')
            else:
                msg_out(nature='error', message='Error: The file related to module information was not found.')


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.option("-k", "--kernel", is_flag=True, help='Display kernel information.')
@click.option("-s", "--shell", is_flag=True, help='Display shell information.')
@click.option("-m", "--module", is_flag=True, help='Display modules information.')
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        option: list = [key for key, value in kwargs.items() if value]
        [get_info(opt) for opt in option] if len(option) > 0 else get_info()


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()
