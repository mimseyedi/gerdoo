"""
                     _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

gerdoolib v1.0.0

gerdoolib is a module to control and manage the gerdooo kernel|shell and its programs.
With the help of this module, you can use pre-written functions for use in the project and
give speed and security to the development of gerdoo.

Fore more information: https://github.com/mimseyedi/gerdoo#gerdoolib
"""


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