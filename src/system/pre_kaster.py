# File for handling stuffs before the program actually start
import sys
import os
from global_var import *
from datetime import datetime
import LogWriter
import traceback


def renew_log_file():
    """
    Delete the log file if 30 days (or more) have passed, and create the log file again
    :return:
    """
    # Get the date when the log file was created
    if os.path.isfile(program_file_dir + "/log.dat"):
        f = open(program_file_dir + "/log.dat", "r")
    else:
        return  # If no log file found then just return
    the_date = f.readline()  # Get the first line of the log file, which gives the time when the log file was created
    f.close()
    del f
    the_date = the_date[29:-1].split("/")  # Get the date from the first line of log file ("Log file created on...")
    the_date = [int(i) for i in the_date]  # Convert string components to int

    # Compare and delete
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    the_date = datetime(year=the_date[2], month=the_date[1], day=the_date[0])
    if (today - the_date).days >= 30:  # Check if 30 days or more have passed since last time created log file
        LogWriter.delete_log_file()  # Remove the log file
        LogWriter.create_log_file()  # Create new, empty log file


def main():
    """
    All processes to be ran on program's startup
    :return:
    """
    # Create program's files path (/usr/share/kaster) if there isn't one
    if not os.path.isdir(program_file_dir):
        os.mkdir(program_file_dir)
    try:
        renew_log_file()
    except ValueError:
        print("An error occurred while the program was refreshing the log file.")
        print("It's likely that the log file was somehow modified.")
        print("=====Traceback=====")
        traceback.print_exc()
