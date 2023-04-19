import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'map.json')


def get_pwd() -> None:
    """
    This function display full path of working directory.

    :return: None
    """

    msg_out(nature='standard', message=os.getcwd())


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(version):
    get_version(PIF) if version else get_pwd()


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()