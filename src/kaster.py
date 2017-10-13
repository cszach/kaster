#!/usr/bin/env python3
"""Kaster Password Vault"""

__author__ = "Nguyen Hoang Duong (NOVAglow on GitHub)"
__license__ = "MIT"
__maintainter__ = "Nguyen Hoang Duong"
__email__ = "novakglow@gmail.com"
__status__ = "Development"

import sys
import os
sys.path.insert(0, "system")
import global_var
import pre_kaster
import LogWriter
import Instructor
sys.path.insert(0, "generator")
import generator

pre_kaster.main()  # Processes to ran on startup

com = sys.argv[1:]
if len(com) == 0:
    Instructor.print_help()
    sys.exit(0)

if com[0] in ["lw", "-lw", "log-writer", "-log-writer"]:
    # Start LogWriter's session
    if len(com) < 2:
        Instructor.print_log_writer_help()
    else:
        if com[1] == "--create-log-file":
            LogWriter.create_log_file()
        elif com[1] == "--new-log-file":
            if os.path.isfile(global_var.log_file_dir):
                os.remove(global_var.log_file_dir)  # Delete the log file if it exists for later renewal
            LogWriter.create_log_file()
        elif com[1] == "--log":
            try:
                with open(global_var.log_file_dir, "a") as f:
                    f.write(" ".join(com[2:]) + "\n")
            except IndexError:
                print("Error: Could not find log string.")
                sys.exit(1)
            except IOError:
                if not os.path.isfile(global_var.log_file_dir):
                    print("Error: Could not find the log file (%s). Try running './kaster.py lw --create-log-file'."
                          % global_var.log_file_dir)
                    sys.exit(1)
                else:
                    print("Run the program as root.")
                    sys.exit(1)
        elif com[1] == "--write-to-log":
            try:
                LogWriter.write_to_log(" ".join(com[2:-1]), True if com[-1] == "0" else False)
            except IndexError:
                print("Error: Could not find log string or option")
                sys.exit(1)
        elif com[1] == "--del-log" or com[1] == "--delete-log-file":
            try:
                os.remove(global_var.log_file_dir)
            except IOError as e:
                if not os.path.isfile(global_var.log_file_dir):
                    print("Error: Could not find the log file (%s)." % global_var.log_file_dir)
                    sys.exit(1)
                else:
                    print("An error has occurred. If permission is denied, try running the program as root.")
                    print("Error:")
                    print(e)
                    sys.exit(1)
        else:
            print("Invalid argument(s).")
            sys.exit(1)


if com[0] in ["g", "-g", "gen", "generate", "generator"]:
    # Start generator session
    if len(com) > 1:
        generator.generator(com[1:])
    else:
        Instructor.print_generator_help()
        sys.exit(0)
