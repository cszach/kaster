# File for handling stuffs before the program actually start
import sys
import os
import global_var
from datetime import datetime, date
import LogWriter


def check_program_file_dir():
    if not os.path.isdir(global_var.program_file_dir):
        LogWriter.create_log_file()


def renew_log_file():
    """
    Delete the log file if 30 days (or more) have passed, and create the log file again
    :return:
    """
    # Get the date when the log file was created
    if os.path.isfile(global_var.log_file_dir):
        f = open(global_var.log_file_dir, "r")
    else:
        check_program_file_dir()
        f = open(global_var.log_file_dir, "r")
    the_date = f.readline()
    f.close()
    del f
    the_date = the_date[29:].split("/")
    the_date = [int(i) for i in the_date]  # Convert string components to int

    # Compare and delete
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    the_date = datetime(year=the_date[2], month=the_date[1], day=the_date[0])
    if (today - the_date).days >= 30:
        if os.path.isfile(global_var.log_file_dir):
            LogWriter.delete_log_file()  # Remove the log file
        LogWriter.create_log_file()  # Create new, empty log file


def main():
    """
    All processes to be ran on program's startup
    :return:
    """
    check_program_file_dir()
    renew_log_file()
