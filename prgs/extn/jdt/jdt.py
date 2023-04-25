import sys
import click
import jaldt
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.parent.__str__())
from mdls.gerdoolib import get_description, get_version, msg_out


PIF: Path = Path(Path(__file__).parent, 'jdt.json')


@click.group(help=get_description(PIF), invoke_without_command=True)
@click.option("--version", is_flag=True, help='Show version of this program.')
def main(**kwargs):
    if kwargs['version']:
        get_version(PIF)
    else:
        if len(sys.argv) == 1:
            msg_out(nature='standard',
                    message="Usage: jdt [OPTIONS] COMMAND [ARGS]...\nTry 'jdt --help' for help.\n\nError: Missing command.")


@main.command(help="Display Jalali calendar in monthly form.")
@click.option('-f', '--farsi', is_flag=True, help="Calendar printing in Farsi language")
@click.argument('month', required=False, type=int)
def cal(**kwargs):
    if kwargs['month'] is None:
        jaldt.calendar(lang='farsi' if kwargs['farsi'] else 'fingilish')
    else:
        if kwargs['month'] in range(1, 13):
            jalali_months = {0: 'now', 1: 'farvardin', 2: 'ordibehesht',
                             3: 'khordad', 4: 'tir', 5: 'mordad',
                             6: 'shahrivar', 7: 'mehr', 8: 'aban',
                             9: 'azar', 10: 'dey', 11: 'bahman', 12: 'esfand'}

            jaldt.calendar(month=jalali_months[kwargs['month']],
                           lang='farsi' if kwargs['farsi'] else 'fingilish')
        else:
            msg_out(nature='error', message='Error: The argument must be between 1 and 12.')


@main.command(help="Converting the Gregorian date to Jalali data.\n\nUsage: jdt g2j [mm] [dd] [yyyy]")
@click.argument('gregorian_date', nargs=3, type=int)
def g2j(**kwargs):
    mm, dd, yyyy = kwargs['gregorian_date']

    jy, jm, jd = jaldt.g2j(yyyy, mm, dd)
    msg_out(nature='standard', message=f"{jy}/{jm}/{jd}")


@main.command(help="Converting the Jalali date to Gregorian data.\n\nUsage: jdt j2g [yyyy] [mm] [dd]")
@click.argument('jalali_date', nargs=3, type=int)
def j2g(**kwargs):
    yyyy, mm, dd = kwargs['jalali_date']

    gy, gm, gd = jaldt.j2g(yyyy, mm, dd)
    msg_out(nature='standard', message=f"{gy}/{gm}/{gd}")


if __name__ == '__main__':
    sys.argv[0] = sys.argv[0][:-3]
    main()