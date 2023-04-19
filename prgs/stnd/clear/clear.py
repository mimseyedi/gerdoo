import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version


PIF: Path = Path(Path(__file__).parent, 'clear.json')


def clear_screen() -> None:
    """
    This function will clear the terminal screen.

    :return: None
    """

    os.system('clear' if os.name == 'posix' else 'cls')


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(version):
    get_version(PIF) if version else clear_screen()


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()