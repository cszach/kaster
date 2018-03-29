# File for handling stuffs before the program actually start
import sys
import os
sys.path.insert(0, "utils")
from global_vars import *


def main():
    """
    All processes to be ran on program's startup
    :return:
    """
    __process__ = "pre_kaster.py (main())"

    if not os.path.isfile(config_path):
        print("FATAL:%s: Could not find Kaster's configuration file (.kasterrc) in home directory" % __process__)
        print("Make sure that you've ran install.sh")
        sys.exit(1)

    # Create program's files path if there isn't one
    if not os.path.isdir(kaster_dir):
        os.mkdir(kaster_dir)

    if not os.path.isfile(log_path):
        open(log_path, "a").close()

    if os.path.getsize(log_path) > 50000000:  # Check if log file's size is larger than 50MB
        os.remove(log_path)
        open(log_path, "a").close()  # Create a new, empty log file
        kaster_logger.info("INFO:%s: Renewed log file" % __process__)
