#!/usr/bin/env python3
"""Kaster Password Vault"""

__author__ = "Nguyen Hoang Duong (NOVAglow on GitHub)"
__license__ = "MIT"
__maintainter__ = "Nguyen Hoang Duong"
__email__ = "novakglow@gmail.com"
__status__ = "Development"

import sys
sys.path.insert(0, "../system")
import global_var
import pre_kaster
import Instructor

pre_kaster.check_program_file_dir()

com = sys.argv[1:]
if len(com) == 0:
    Instructor.print_help()
    sys.exit(0)
