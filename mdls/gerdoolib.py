"""
                     _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

gerdoolib

gerdoolib is a module to control and manage the gerdooo kernel|shell and its programs.
With the help of this module, you can use pre-written functions for use in the project and
give speed and security to the development of gerdoo.

Fore more information: https://github.com/mimseyedi/gerdoo#gerdoolib
"""


import json
import hashlib
from pathlib import Path


def msg_out(nature: str, message: str) -> None:
    """
    The task of this function is to display the message in the format and style of gerdooo.

    :param nature: Messages type -> ['standard', 'success', 'error', 'warning']
    :param message: The message in string format.
    :return: None
    """

    if not isinstance(nature, str) or nature not in ['standard', 'success', 'error', 'warning']:
        raise TypeError(
            "nature argument must be in the form of a str and be chosen between ['standard', 'success', 'error', 'warning'].")

    if not isinstance(message, str):
        raise TypeError("message argument must be in the form of a str.")

    RESET   = '\033[0m'
    ERROR   = '\033[91m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'

    match nature:
        case 'standard':
            print(f"{RESET}{message}{RESET}")
        case 'error':
            print(f"{ERROR}{message}{RESET}")
        case 'success':
            print(f"{SUCCESS}{message}{RESET}")
        case 'warning':
            print(f"{WARNING}{message}{RESET}")


def get_version(pif_path: str|Path) -> None:
    """
    The task of this function is to display the version of programs.

    :param pif_path: The path of the PIF.
    :return: None
    """

    if not isinstance(pif_path, (str, Path)):
        raise TypeError("pif_path argument must be in the form of a str or pathlib.Path.")

    pif_path: Path = Path(pif_path) if isinstance(pif_path, str) else pif_path

    if pif_path.exists() and len(pif_path.read_text()) > 0:
        with open(pif_path, 'r') as pif:
            try:
                msg_out(nature='standard', message=json.load(pif)['version'])
            except KeyError:
                msg_out(nature='error', message='Error: Program Information File is broken!')
            except json.JSONDecodeError:
                msg_out(nature='error', message='Error: Program Information File is broken!')
    else:
        msg_out(nature='error', message=f'Error: Program Information File not found!')


def get_description(pif_path: str|Path) -> bool|str:
    """
    The task of this function is to display the program description in help (--help) option.

    :param pif_path: The path of the PIF.
    :return: str
    """

    if not isinstance(pif_path, (str, Path)):
        raise TypeError("pif_path argument must be in the form of a str or pathlib.Path.")

    pif_path: Path = Path(pif_path) if isinstance(pif_path, str) else pif_path

    if pif_path.exists() and len(pif_path.read_text()) > 0:
        with open(pif_path, 'r') as pif:
            try:
                return json.load(pif)['description']
            except KeyError: ...
            except json.JSONDecodeError: ...

    return False


def str_to_sha256(string: str) -> str:
    """
    This function takes a string as an argument and returns a hashed string with sha256 algorithm.

    :param string: This function takes a string as an argument and returns a hashed string with sha256 algorithm.
    :return: str
    """

    if not isinstance(string, str):
        raise TypeError("string argument must be in the form of a str.")

    algorithm= hashlib.sha256()
    algorithm.update(string.encode("UTF-8"))
    return algorithm.hexdigest()


def authentication(tkn_pass: str, pass_file: str|Path) -> bool:
    """
    The task of this function is user authentication.

    :param tkn_pass: Password taken from the user.
    :param pass_file: User's passwords file.
    :return: bool
    """

    if not isinstance(tkn_pass, str):
        raise TypeError("tkn_pass argument must be in the form of a str.")

    if not isinstance(pass_file, (str, Path)):
        raise TypeError("pass_file argument must be in the form of a str or pathlib.Path.")

    pass_file: Path = Path(pass_file) if isinstance(pass_file, str) else pass_file

    if not pass_file.exists() or not pass_file.is_file() or pass_file.suffix != '.json':
        raise FileNotFoundError("The pass_file argument must exist and be a json file.")

    with open(pass_file, 'r') as passwords:
        try:
            user_pass = json.load(passwords)['user_pass']
        except KeyError:
            raise KeyError("'user_pass' key not found!")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"'{pass_file}' is broken!", doc=pass_file.__str__(), pos=0)

    return True if str_to_sha256(tkn_pass) == user_pass else False
