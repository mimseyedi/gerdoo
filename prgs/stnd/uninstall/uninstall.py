import sys
import click
import shutil
from pathlib import Path
from getpass import getpass

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out, authentication


PIF: Path = Path(Path(__file__).parent, 'uninstall.json')


def find_prg(program: str) -> bool|Path:
    """
    The task of this function is to find programs and return their path.

    :param program: Programs name in string format.
    :return: bool|Path
    """

    bins: Path = Path(Path(__file__).parent.parent.parent.parent, 'krnl', 'bins', program)

    stnd: Path = Path(Path(__file__).parent.parent, program)

    extn: Path = Path(Path(__file__).parent.parent.parent, 'extn', program)

    return bins if bins.exists() else (stnd if stnd.exists() else (extn if extn.exists() else False))


@click.command(help=get_description(PIF))
@click.option('--version', is_flag=True, help="Show version of this program.")
@click.argument('program', required=False)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if kwargs['program'] is None:
            msg_out(nature='standard',
                    message="Usage: uninstall [OPTIONS] [PROGRAM]\nTry 'uninstall --help' for help.\n\nError: Missing argument -> 'PROGRAM'.")
        else:
            prg_status: bool|Path = find_prg(program=kwargs['program'])

            if isinstance(prg_status, Path):
                auth_pass = getpass()
                if authentication(tkn_pass=auth_pass,
                                  pass_file=Path(Path(__file__).parent.parent.parent.parent, 'setg', 'PASS.json')):

                    shutil.rmtree(prg_status)

                    msg_out(nature='success',
                            message=f"The '{kwargs['program']}' program has been successfully uninstalled.")
                else:
                    msg_out(nature='error', message='Error: Authentication failed!')
            else:
                msg_out(nature='error', message=f"Error: The '{kwargs['program']}' Program was not found!")


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()