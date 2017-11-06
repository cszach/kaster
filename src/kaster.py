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
sys.path.insert(0, "generator")
import generator

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
                                "lw", "gen",
                                "create", "append=", "log=", "clear", "delete",
                                "length=", "duplicate=", "upper", "lower", "number", "symbol",
                                "output="])
except getopt.GetoptError as e:
    print("Error: ", end="")
    print(e)
    print("Pass option '-h' or '--help' to see the available options and arguments")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        Instructor.main(None)
        sys.exit(0)
    elif opt == "--version":
        print(__program__)
        print("Version " + __version__)
        sys.exit(0)
    elif opt == "--lw":
        LogWriter.lw_main(opts[1:])
        sys.exit(0)
    elif opt == "--gen":
        try:
            generator.generator(opts[1:])
        except KeyboardInterrupt:
            print()
            print("Got keyboard interruption, quitting...")
        finally:
            sys.exit(0)
    else:
        print("Error: Wrong use of option '%s'. Quitting..." % opt)
        sys.exit(1)

print("Error: Invalid argument '%s'. Quitting..." % args[0])
