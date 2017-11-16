import sys
import os
from global_var import *
from k_date import k_now
import Instructor


# Kaster' log file manipulator, deals everything that involves the log file


def create_log_file():
    """
    Create program's log file (log.dat) in /usr/share/kaster
    :return:
    """
    if not os.path.isdir(program_file_dir):  # Check program's directory existence
        os.mkdir(program_file_dir)  # If the directory does not exist then create one
    if not os.path.isfile(program_file_dir + "/log.dat"):
        open(program_file_dir + "/log.dat", "a").close()  # Create empty log file
    with open(program_file_dir + "/log.dat", "w") as f:
        f.write("Log file created on %s\n" % k_now(time_format, date_format))
    del f


def write_to_log(log_str):
    """
    Write log message to log file
    :param log_str: The log message to be written to the log file
    :return:
    """
    if not os.path.isfile(program_file_dir + "/log.dat"):
        create_log_file()
    with open(program_file_dir + "/log.dat", "a") as f:
        f.write(("[%s] %s" + "\n") % (k_now(time_format, date_format), log_str))


def delete_log_file():
    """
    Delete the log file
    :return:
    """
    if os.path.isfile(program_file_dir + "/log.dat"):
        os.remove(program_file_dir + "/log.dat")


def lw_main(com_list):
    """
    Main process of the log writer, called by the main program
    :param com_list: Input arguments
    :return:
    """
    if len(com_list) == 0:
        Instructor.main("man_lw.txt")
        sys.exit(0)
    for l_idx, (l_opt, l_arg) in enumerate(com_list):
        if l_opt in ("-h", "--help"):
            Instructor.main("man_lw.txt")
        elif l_opt == "--create":
            create_log_file()
        elif l_opt == "--append":
            if os.path.isfile(program_file_dir + "/log.dat"):
                with open(program_file_dir + "/log.dat", "a") as f:
                    f.write(l_arg + "\n")
                del f

            else:
                if input("Log file does not exist, create one and write now? [Y|N] ").lower() == "y":
                    create_log_file()
                    lw_main([(l_opt, l_arg)] + com_list[l_idx + 1:])
                    break
        elif l_opt == "--log":
            if os.path.isfile(program_file_dir + "/log.dat"):
                write_to_log(l_arg)
            else:
                if input("Log file does not exist, create one and write now? [Y|N] ").lower() == "y":
                    create_log_file()
                    lw_main([(l_opt, l_arg)] + com_list[l_idx + 1:])
                    break
        elif l_opt == "--clear":
            if os.path.isfile(program_file_dir + "/log.dat"):
                os.remove(program_file_dir + "/log.dat")
                create_log_file()
            else:
                print("Log file does not exist")
        elif l_opt == "--delete":
            delete_log_file()
        else:
            print("Error: Not recognized option '%s'. Quitting..." % l_opt)
            sys.exit(1)
