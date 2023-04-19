import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'items.json')


def show_items() -> None:
    ITEMS_IN_ROW: int = os.get_terminal_size()[0] // 25

    items = sorted([item[:20] + "...  " if len(item) > 23 else item + (" " * (25 - len(item))) for item in os.listdir()])

    index, start, end = 0, 0, ITEMS_IN_ROW

    while index < len(os.listdir()):
        msg_out(nature='standard', message=''.join(items[start:end]))
        start += ITEMS_IN_ROW
        end   += ITEMS_IN_ROW
        index += ITEMS_IN_ROW


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(**kwargs):
    get_version(PIF) if kwargs['version'] else show_items()


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()