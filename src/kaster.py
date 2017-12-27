#!/usr/bin/env python3
"""Kaster Password Vault"""

__program__ = "Kaster Password Vault"
__version__ = "Beta"
__author__ = "Nguyen Hoang Duong"
__license__ = "MIT"
__maintainter__ = "Nguyen Hoang Duong"
__email__ = "novakglow@gmail.com"
__status__ = "Production"

import sys
import os
import getopt
import logging
sys.path.insert(0, "system")
import pre_kaster
import Instructor
sys.path.insert(0, "utils")
from k_path import *
sys.path.insert(0, "generator")
from generator import generator
sys.path.insert(0, "vault")
from vault import vault


# Check if the user has logged in as root
if os.getenv("SUDO_USER") is None:
    print("Please run Kaster as root")
    sys.exit(1)

pre_kaster.main()  # Processes to ran on startup
__process__ = "kaster.py (MAIN)"

if len(sys.argv[1:]) == 0:
    # Print help if no argument/option is specified
    Instructor.main(None)
    sys.exit(0)

logging.basicConfig(filename="%s" % log_path,
                    format="[%(asctime)s] %(message)s",
                    datefmt="%s %s" % (time_format, date_format),
                    level=logging.INFO)

# Get all the arguments specified
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "ha:l:d:o:",
                               ["help", "version", "info",
                                "gen", "vault",
                                "length=", "duplicate=", "upper", "lower", "number", "symbol",
                                "output=",
                                "account", "new", "list", "get=", "getpass=", "edit=", "del=", "delall",
                                "name=", "login=", "password=", "comment="])
except getopt.GetoptError as e:
    logging.error("FATAL:%s: %s" % (__process__, e))
    print("Pass option '-h' or '--help' to see the available options and arguments")
    sys.exit(2)

# Iterate over options among with their arguments to check for duplicate
scanned_opt = []
try:
    for opt, arg in opts:
        if opt in scanned_opt:
            logging.error("FATAL:%s: Found duplicate option %s" % (__process__, opt))
            sys.exit(1)
        else:
            scanned_opt.append(opt)
finally:
    del scanned_opt

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
    elif opt == "--gen":
        try:
            generator(opts[1:])
        except KeyboardInterrupt:
            print()
            print("Got keyboard interruption, quitting...")
            sys.exit(0)
    elif opt == "--vault":
        # Might remove this try except and handle keyboard interruption in vault.vault() instead
        try:
            vault(opts[1:])
        except KeyboardInterrupt:
            print()
            print("Got keyboard interruption, quitting...")
    else:
        logging.error("FATAL:%s: Wrong usage of option '%s'." % (__process__, opt))
        sys.exit(1)
    del opts, args
    sys.exit(0)

logging.error("FATAL:%s: Invalid argument '%s'." % (__process__, args[0]))
sys.exit(1)
