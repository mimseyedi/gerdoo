import os
import sys
import click
import shutil
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'deldir.json')


def del_directory(dir_path: str|Path, force: bool=False) -> None:
    """
    This function deletes a directory.

    :param dir_path: The directory path.
    :param force: To remove the full directory.
    :return: None
    """

    dir_path = Path(os.getcwd(), dir_path) if isinstance(dir_path, str) else dir_path

    if dir_path.exists():
        if dir_path.is_dir():
            if len(os.listdir(dir_path)) > 0:
                if force:
                    shutil.rmtree(dir_path)
                    msg_out(nature='success', message=f"The directory named '{dir_path.name}' was successfully deleted.")
                else:
                    msg_out(nature='error', message=f"Error: The directory named '{dir_path.name}' is full!")
            else:
                os.rmdir(dir_path)
                msg_out(nature='success', message=f"The directory named '{dir_path.name}' was successfully deleted.")

        else:
            msg_out(nature='error', message=f"Error: '{dir_path.name}' is not a directory!")
    else:
        msg_out(nature='error', message=f"Error: A directory named '{dir_path.name}' was not found in this path : '{dir_path.parent}'")


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.option("-f", "--force", is_flag=True, help='To delete directories that are full.')
@click.argument('directory', required=False)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if kwargs['directory'] is None:
            msg_out(nature='standard',
                    message="Usage: deldir [OPTIONS] [DIRECTORY]\nTry 'deldir --help' for help.\n\nError: Missing argument -> 'DIRECTORY'.")
        else:
            del_directory(kwargs['directory']) if not kwargs['force'] else del_directory(kwargs['directory'], True)


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()