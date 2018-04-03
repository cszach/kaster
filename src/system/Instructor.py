"""
system/Instructor.py - Facility for printing manual pages of Kaster and Kaster's subprograms

Copyright (C) 2017-2018 Nguyen Hoang Duong <novakglow@gmail.com>
Licensed under MIT License (see LICENSE).
"""

import sys
sys.path.insert(0, "../utils")
from global_vars import *


def main(man_page_name):
    """
    Main process for Instructor
    :param man_page_name: File name of the manual. If it's None, print all manual pages.
    :return: 200 if operation success
              201 if a manual page doesn't exist (doesn't happen if the user doesn't do anything with the manual files)
    """
    __process__ = "Instructor.py -> main()"

    if man_page_name is None:
        # Read all the manual pages
        print("Kaster Password Vault's help")
        print()
        man_pages = ["man_generic.txt", "man_gen.txt", "man_vault.txt"]
        for man in man_pages:
            main(man)
            input()
        del man, man_pages
    else:
        # Read specified manual page
        try:
            f = open("manual/" + man_page_name, "r")
        except FileNotFoundError:
            kaster_logger.error("%s: Couldn't find manual page: %s" % (__process__, man_page_name))
            return 201
        f_content = f.read()
        f.close()
        print(f_content)
        del f, f_content

    return 200
