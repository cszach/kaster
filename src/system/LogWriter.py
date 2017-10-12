import sys
import os
import global_var
from k_date import date, time


# Kaster' log file manipulator, deals everything that involves the log file
origin = os.getcwd()


def create_log_file():
    """
    Create program's log file (log.dat) in /usr/share/kaster
    :return:
    """
    try:
        if not os.path.isdir(global_var.program_file_dir):
            os.mkdir(global_var.program_file_dir)
        if not os.path.isfile(global_var.log_file_dir):
            open(global_var.log_file_dir, 'a').close()  # Create empty log file
        with open(global_var.log_file_dir, "w") as f:
            f.write("Log file created on %s." % (date(kaster.date_format)))
        del f
    except Exception as e:
        print("An error has occurred. If permission is denied, try running the program as root.")
        print("Error:")
        print(e)
        sys.exit(1)


def write_to_log(log_str, print_log):
    """
    Write log message to log file
    :param log_str: The log message to be written to the log file
    :param print_log: Print log message to the console or not (boolean)
    :return:
    """
    try:
        if print_log:
            print(log_str)
        with open(global_var.log_file_dir, "a") as f:
            f.write(("[%s %s] %s" + "\n") % (time(global_var.time_format), date(global_var.date_format), log_str))
    except IOError as e:
        if not os.path.isfile(global_var.log_file_dir):
            self.create_log_file()
            print("Error: Log file was not found. Outputs weren't saved.")
        else:
            print("Run the program as root")


def delete_log_file():
    """
    Delete the log file
    :return:
    """
    if os.path.isfile(global_var.log_file_dir):
        os.remove(global_var.log_file_dir)
