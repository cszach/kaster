# File for handling stuffs before the program actually start
import sys
import os
import global_var
from datetime import datetime
import LogWriter


def check_program_file_dir():
    """
    Check if the program's file directory exists (/usr/share/kaster)
    If it does not, call create_log_file() function of the log writer,
    which creates the program's file directory and then the log file in that directory
    :return:
    """
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
        return  # If no log file found then just return
    the_date = f.readline()  # Get the first line of the log file, which gives the time when the log file was created
    f.close()
    del f
    the_date = the_date[29:-1].split("/")  # Get the date from the first line of log file ("Log file created on...")
    the_date = [int(i) for i in the_date]  # Convert string components to int

    # Compare and delete
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    try:
        the_date = datetime(year=the_date[2], month=the_date[1], day=the_date[0])
    except ValueError:
        print("Warning: Failed to perform a start-up operation. Check the log file to see details.")
        LogWriter.write_to_log("Fail to get the date on which the log file was created.")
        return
    if (today - the_date).days >= 30:  # Check if 30 days or more have passed since last time created log file
        LogWriter.delete_log_file()  # Remove the log file
        LogWriter.create_log_file()  # Create new, empty log file


def main():
    """
    All processes to be ran on program's startup
    :return:
    """
    check_program_file_dir()
    renew_log_file()
