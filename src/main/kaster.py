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
sys.path.insert(0, "../generator")
import generator

pre_kaster.check_program_file_dir()

com = sys.argv[1:]
if len(com) == 0:
    Instructor.print_help()
    sys.exit(0)

if com[0] in ["g", "-g", "gen", "generate", "generator"]:
    # Start generator session
    if len(com) > 1:
        generator.generator(com[1:])
    else:
        Instructor.print_generator_help()
