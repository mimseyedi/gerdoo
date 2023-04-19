import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'system.json')


def get_system_information(option: str) -> None:
    """
    This function display general system information.

    {'all': 'all information',
     'system': 'system name',
     'node': 'node name',
     'kernel': 'kernel release',
     'os': 'operating system version',
     'machine': 'system architecture'}

    :return: None
    """

    match option:
        case 'all':
            msg_out(nature='standard', message=f"System name: {os.uname()[0]}")
            msg_out(nature='standard', message=f"Node name: {os.uname()[1]}")
            msg_out(nature='standard', message=f"Kernel releae: {os.uname()[2]}")
            msg_out(nature='standard', message=f"Os version: {os.uname()[3]}")
            msg_out(nature='standard', message=f"Architecture: {os.uname()[4]}")
        case 'system':
            msg_out(nature='standard', message=os.uname()[0])
        case 'node':
            msg_out(nature='standard', message=os.uname()[1])
        case 'kernel':
            msg_out(nature='standard', message=os.uname()[2])
        case 'os':
            msg_out(nature='standard', message=os.uname()[3])
        case 'machine':
            msg_out(nature='standard', message=os.uname()[4])


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.option("-a", "--all", is_flag=True, help='Display all general system info.')
@click.option("-s", "--system", is_flag=True, help='Display system name. ')
@click.option("-n", "--node", is_flag=True, help='Display node name.')
@click.option("-k", "--kernel", is_flag=True, help='Display kernel release.')
@click.option("-o", "--os", is_flag=True, help='Display operating system version.')
@click.option("-m", "--machine", is_flag=True, help='Display system architecture.')
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        option: list = [key for key, value in kwargs.items() if value]
        [get_system_information(opt) for opt in option] if len(option) > 0 else get_system_information('all')


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()