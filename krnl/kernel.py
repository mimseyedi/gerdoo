"""
                     _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

kernel v1.0.0

The gerdooo kernel is placed behind the shell and connects user commands to programs.
The kernel interprets the user's commands, which it receives through the shell, and
manages and controls the execution of the programs.

For more information: https://github.com/mimseyedi/gerdoo#kernel
"""


import os
import sys
import json
import typing
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.__str__())
import mdls.gerdoolib as gerdoolib

from krnl.bins.back import back as back_program
from krnl.bins.bash import bash as bash_program
from krnl.bins.goto import goto as goto_program
from krnl.bins.home import home as home_program
from krnl.bins.path import path as path_program
from krnl.bins.void import void as void_program


def find_prg(program: str) -> bool|Path|typing.Callable:
    """
    The task of this function is to find programs and return their path.

    :param program: Programs name in string format.
    :return: False|Path|Callable
    """

    # Built-in prgoram func:
    bins: dict = {back_program.back.__name__: back_program.back,
                  bash_program.bash.__name__: bash_program.bash,
                  goto_program.goto.__name__: goto_program.goto,
                  home_program.home.__name__: home_program.home,
                  path_program.path.__name__: path_program.path,
                  void_program.void.__name__: void_program.void}

    # Standard program path:
    stnd: Path = Path(Path(__file__).parent.parent, 'prgs/stnd/', program)

    # External program path:
    extn: Path = Path(Path(__file__).parent.parent, 'prgs/extn/', program)

    return bins[program] if program in bins else (stnd if stnd.exists() else (extn if extn.exists() else False))


def read_pif(pif_path: str|Path) -> bool|dict:
    """
    This function reads the required information of each program from the
    PIF (Program Information File) of the specified program and returns it in the form of a dictionary.

    :param pif_path: The path of the PIF.
    :return: False|dict
    """

    pif_path: Path = Path(pif_path) if isinstance(pif_path, str) else pif_path

    return json.loads(pif_path.read_text(encoding='utf-8')) if pif_path.exists() and len(pif_path.read_text()) > 0 else False


def execute(program: str, args: list=None) -> None:
    """
    This is the main kernel function.
    The task of this function is to respond to user requests and execute and manage programs.

    :param program: The name of the program to be executed.
    :param args: Arguments that need to be passed to the program.
    :return: None
    """

    # Create user's command in form of a list:
    command: list = [program, *args] if args is not None else [program]

    # Find Program to execute:
    executable_program: bool|Path|typing.Callable = find_prg(program=program)

    if isinstance(executable_program, typing.Callable):
        # Execute built-in programs:
        executable_program(command)

    elif isinstance(executable_program, Path):
        # Reading Program Information File (PIF):
        pif: bool|dict = read_pif(pif_path=Path(executable_program, f'{program}.json'))

        if isinstance(pif, dict):
            try:
                if pif['executable'] == f'{program}.py':
                    out_path: Path = Path(executable_program, pif['executable'])
                    os.system(f"{sys.executable} {out_path.__str__()} {' '.join(command[1:])}")
                else:
                    gerdoolib.msg_out(nature='error',
                                      message=f'Error: Unfortunately, this program is not supported -> ({program})')

            except KeyError:
                gerdoolib.msg_out(nature='error', message='Error: Program Information File is broken!')
        else:
            if any(True for char in './' if char in program):
                gerdoolib.msg_out(nature='error', message=f'Error: Program not found -> ({program})')
            else:
                gerdoolib.msg_out(nature='error', message=f'Error: Program Information File not found!')
    else:
        gerdoolib.msg_out(nature='error', message=f'Error: Program not found -> ({program})')
