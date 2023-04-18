import sys
import click
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, str_to_sha256, msg_out


PIF: Path = Path(Path(__file__).parent, 'hash.json')
sys.argv[0] = sys.argv[0][:-3]


@click.command(help=get_description(PIF))
@click.option("--version", is_flag=True, help='Show version of this program.')
@click.option("--sha256", is_flag=True, help='Hashing a string with sha256 algorithm')
@click.argument('text', required=False)
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if kwargs['text'] is None:
            msg_out(nature='standard',
                    message="Usage: hash [OPTIONS] [TEXT]\nTry 'hash --help' for help.\n\nError: Missing argument -> 'TEXT'.")
        else:
            if kwargs['sha256']:
                msg_out(nature='standard', message=str_to_sha256(kwargs['text']))
            else:
                msg_out(nature='standard',
                        message="Usage: hash [OPTIONS] [TEXT]\nTry 'hash --help' for help.\n\nError: Missing hashing algorithm option.")


if __name__ == '__main__':
    main()