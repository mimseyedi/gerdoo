import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'newdir.json')
sys.argv[0] = sys.argv[0][:-3]


def new_directory(dir_path: str|Path) -> None:
    """
    This function creates a directory.

    :param dir_path: The directory path.
    :return: None
    """

    dir_path = Path(os.getcwd(), dir_path) if isinstance(dir_path, str) else dir_path

    if not dir_path.exists():
        os.mkdir(dir_path)
        msg_out(nature='success', message=f"The directory named '{dir_path.name}' was successfully created.")
    else:
        msg_out(nature='error', message=f"Error: A directory named '{dir_path.name}' already exists in this path: '{dir_path.parent}'")


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.argument('directories', required=False, nargs=-1)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(kwargs['directories']) == 0:
            msg_out(nature='standard',
                    message="Usage: newdir [OPTIONS] [DIRECTORIES]...\nTry 'newdir --help' for help.\n\nError: Missing argument -> 'DIRECTORIES'.")
        else:
            for dir_ in kwargs['directories']:
                new_directory(dir_path=dir_)


if __name__ == '__main__':
    main()