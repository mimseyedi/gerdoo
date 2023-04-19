import os
import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'delf.json')


def del_file(file_path: str|Path) -> None:
    """
    This function deletes a file.

    :param file_path: The file path.
    :return: None
    """

    file_path = Path(os.getcwd(), file_path) if isinstance(file_path, str) else file_path

    if file_path.exists():
        if file_path.is_file():
            os.remove(file_path)
            msg_out(nature='success', message=f"The file named '{file_path.name}' was successfully deleted.")
        else:
            msg_out(nature='error', message=f"Error: '{file_path.name}' is not a file!")
    else:
        msg_out(nature='error', message=f"Error: A file named '{file_path.name}' was not found in this path: '{file_path.parent}'")


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.argument('files', required=False, nargs=-1)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(kwargs['files']) == 0:
            msg_out(nature='standard',
                    message="Usage: delf [OPTIONS] [FILES]...\nTry 'delf --help' for help.\n\nError: Missing argument -> 'FILES'.")
        else:
            for file in kwargs['files']:
                del_file(file_path=file)


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()