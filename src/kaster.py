#!/usr/bin/env python3
"""
Kaster Password Vault - Simple password manager for GNU/Linux platform

Copyright (C) 2017-2018 Nguyen Hoang Duong <novakglow@gmail.com>
Licensed under MIT License (see LICENSE).
"""

__program__ = "Kaster Password Vault"
__version__ = "Beta"
__author__ = "Nguyen Hoang Duong"
__license__ = "MIT"
__maintainter__ = "Nguyen Hoang Duong"
__email__ = "novakglow@gmail.com"
__status__ = "Production"

import sys
import os
import logging
import getopt
sys.path.insert(0, "system")
import pre_kaster
import Instructor
sys.path.insert(0, "utils")
from global_vars import *
sys.path.insert(0, "generator")
from generator import generator
sys.path.insert(0, "vault")
from vault import vault

# TODO: Check if the user has logged in as root
if os.getenv("SUDO_USER") is None:
    print("Please run Kaster as root")
    sys.exit(9)

pre_kaster.main()  # Processes to ran on startup
__process__ = "kaster.py (MAIN)"

# TODO: Print help if no argument/option is specified
if len(sys.argv[1:]) == 0:
    Instructor.main(None)
    sys.exit(3)

# TODO: Get all the arguments specified
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "ha:l:d:o:",
                               ["help", "version", "info", "verbose",
                                "gen", "vault",
                                "length=", "duplicate=", "upper", "lower", "number", "symbol",
                                "output=",
                                "account", "new", "list", "get=", "getpass=", "edit=", "del=", "delall",
                                "name=", "login=", "password=", "comment="])
except getopt.GetoptError as e:
    kaster_logger.critical("%s: %s" % (__process__, e))
    print("Pass option '-h' or '--help' to see the available options and arguments")
    sys.exit(4)

# TODO: Iterate over options among with their arguments to check for duplicate
scanned_opt = []
try:
    for opt, arg in opts:
        if opt in scanned_opt:
            kaster_logger.error("%s: Found duplicate option %s" % (__process__, opt))
            sys.exit(8)
        else:
            scanned_opt.append(opt)
finally:
    del scanned_opt

# TODO: Iterate over options
for opt, arg in opts:
    if opt in ("-h", "--help"):
        Instructor.main(None)

    elif opt == "--version":
        print(__program__)
        print("Version " + __version__)

    elif opt == "--info":
        print(__program__ + " " + __version__)
        print("Kaster Password Vault is a CLI offline password manager.")
        print("Brought to you by " + __author__)

    elif opt == "--verbose":
        kaster_logger.removeHandler(o_handler)
        o_handler.setLevel(logging.INFO)
        kaster_logger.addHandler(o_handler)

    elif opt == "--gen":
        try:
            sys.exit(generator(opts[1:]))
        except KeyboardInterrupt:
            print()
            kaster_logger.info("Generator: Got keyboard interruption, quitting...")
            sys.exit(707)

    elif opt == "--vault":
        # Might remove this try except and handle keyboard interruption in vault.vault() instead
        try:
            sys.exit(vault(opts[1:]))
        except KeyboardInterrupt:
            print()
            kaster_logger.info("Vault: Got keyboard interruption, quitting...")
            sys.exit(0)

    else:
        kaster_logger.error("%s: Wrong usage of option '%s'." % (__process__, opt))
        sys.exit(6)

    del opts, args
    sys.exit(0)

kaster_logger.error("%s: Invalid argument '%s'." % (__process__, args[0]))
sys.exit(1)
