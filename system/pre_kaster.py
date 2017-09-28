# File for handling stuffs before the program actually start
import sys
import os
import global_var


def check_program_file_dir():
    if not os.path.isdir(global_var.program_file_dir):
        os.mkdir(global_var.program_file_dir)
