"""
system/pre_kaster.py - Tasks to be done when the program is initialized

Copyright (C) 2017-2018 Nguyen Hoang Duong <you_create@protonmail.com>
Licensed under MIT License (see LICENSE).
"""

import sys
import os
sys.path.insert(0, "utils")
from global_vars import *

__process__ = "pre_kaster.py -> main()"

if not os.path.isfile(config_path):
    kaster_logger.critical(":%s: Could not find Kaster's configuration file (.kasterrc) in home directory" % __process__)
    print("Make sure that you've ran install.sh")
    sys.exit(104)

# Create program's files path if there isn't one
if not os.path.isdir(kaster_dir):
    os.mkdir(kaster_dir)

if not os.path.isfile(log_path):
    open(log_path, "a").close()
    return 102

if os.path.getsize(log_path) > 50000000:  # Check if log file's size is larger than 50MB
    os.remove(log_path)
    open(log_path, "a").close()  # Create a new, empty log file
    kaster_logger.info("%s: Renewed log file" % __process__)

return 100
