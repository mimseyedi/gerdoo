"""
                     _
                    | |
   __ _  ___ _ __ __| | ___   ___
  / _` |/ _ \ '__/ _` |/ _ \ / _ \
 | (_| |  __/ | | (_| | (_) | (_) |
  \__, |\___|_|  \__,_|\___/ \___/
   __/ |
  |___/

gerdoo

gerdoo is a personal CLI assistant.
gerdoo can run smaller programs and simulate and personalize the terminal environment.

To participate in this project and for more information, refer to the following link:
https://github.com/mimseyedi/gerdoo

"""


import os
import sys
from pathlib import Path


PYTHON_VERSION: tuple = (3, 11)


def main():
    if sys.version_info[0] >= PYTHON_VERSION[0] and sys.version_info[1] >= PYTHON_VERSION[1]:

        shell_exec_path: Path = Path('shll', 'shell.py')

        if shell_exec_path.exists():

            updater_path: Path = Path('updt', 'gerdoo_updater.py')

            if updater_path.exists():
                os.system(f"{sys.executable} {updater_path.__str__()}")

            os.system(f"{sys.executable} {shell_exec_path.__str__()}")
        else:
            print("\033[91mError: The files are damaged. Please reinstall the program or visit the link below for help and more information.\033[0m")
            print("       https://github.com/mimseyedi/gerdoo")
    else:
        print("\033[91mError: You need Python 3.11 or higher to run this program.\033[0m")
        print("       \033[91mDownload from this link: \033[0mhttps://www.python.org/downloads/")

        
if __name__ == '__main__':
    main()
