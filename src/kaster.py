#!/usr/bin/env python3
"""Kaster Password Vault"""

__program__ = "Kaster Password Vault"
__version__ = "Beta"
__author__ = "Nguyen Hoang Duong (NOVAglow on GitHub)"
__license__ = "MIT"
__maintainter__ = "Nguyen Hoang Duong"
__email__ = "novakglow@gmail.com"
__status__ = "Development"

import sys
import os
import getopt
sys.path.insert(0, "system")
import global_var
import pre_kaster
import LogWriter
import Instructor
import k_std
sys.path.insert(0, "generator")
import generator
sys.path.insert(0, "vault")
import vault

# Check if the user has logged in as root
if os.getenv("SUDO_USER") is None:
    print("Please run Kaster as root")
    sys.exit(1)

pre_kaster.main()  # Processes to ran on startup

if len(sys.argv[1:]) == 0:
    # Print help if no argument/option is specified
    Instructor.main(None)
    sys.exit(0)

# Get all the arguments specified
try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "ha:l:d:o:",
                               ["help", "version", "info",
                                "lw", "gen", "vault",
                                "create", "append=", "log=", "clear", "delete",
                                "std=",
                                "length=", "duplicate=", "upper", "lower", "number", "symbol",
                                "output=",
                                "account", "new", "list", "get=", "getpass=", "del=", "delall",
                                "name=", "login=", "password=", "comment="])
except getopt.GetoptError as e:
    print("Error: ", end="")
    print(e)
    print("Pass option '-h' or '--help' to see the available options and arguments")
    sys.exit(2)

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
    elif opt == "--lw":
        LogWriter.lw_main(opts[1:])
    elif opt == "--std":
        if k_std.check_std(arg) == 0:
            k_std.read_std(arg)
    elif opt == "--gen":
        try:
            generator.generator(opts[1:])
        except KeyboardInterrupt:
            print()
            print("Got keyboard interruption, quitting...")
    elif opt == "--vault":
        # Might remove this try except and handle keyboard interruption in vault.vault() instead
        try:
            vault.vault(opts[1:])
        except KeyboardInterrupt:
            print()
            print("Got keyboard interruption, quitting...")
    else:
        print("Error: Wrong use of option '%s'. Quitting..." % opt)
        sys.exit(1)
    sys.exit(0)

print("Error: Invalid argument '%s'. Quitting..." % args[0])
sys.exit(1)
