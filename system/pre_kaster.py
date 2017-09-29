# File for handling stuffs before the program actually start
import sys
import os
import global_var
from LogWriter import LogWriter

k_log_writer = LogWriter()


def check_program_file_dir():
    if not os.path.isdir(global_var.program_file_dir):
        k_log_writer.create_log_file()
