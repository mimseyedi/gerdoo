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
from pathlib import Path


def find_prg(program: str) -> bool|Path:
    """
    The task of this function is to find programs and return their path.

    :param program: Programs name in string format.
    :return: False|Path
    """

    # Built-in prgoram path:
    bins: Path = Path(Path(__file__).parent, 'bins/', program)

    # Standard program path:
    stnd: Path = Path(Path(__file__).parent.parent, 'prgs/stnd/', program)

    # External program path:
    extn: Path = Path(Path(__file__).parent.parent, 'prgs/extn/', program)

    return bins if bins.exists() else (stnd if stnd.exists() else (extn if extn.exists() else False))


def read_pif(pif_path: str|Path) -> bool|dict:
    """
    This function reads the required information of each program from the
    PIF (Program Information File) of the specified program and returns it in the form of a dictionary.

    :param pif_path: The path of the PIF.
    :return: False|dict
    """

    pif_path: Path = Path(pif_path) if isinstance(pif_path, str) else pif_path

    return json.loads(pif_path.read_text(encoding='utf-8')) if pif_path.exists() else False


def execute(program: str, args: list=None) -> None:
    """
    This is the main kernel function.
    The task of this function is to respond to user requests and execute and manage programs.

    :param program: The name of the program to be executed.
    :param args: Arguments that need to be passed to the program.
    :return: None
    """

    pass
