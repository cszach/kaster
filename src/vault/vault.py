import sys
import os
sys.path.insert(0, "../system")
import Instructor


def v_main(com_list):
    """
    Main program for the vault
    :param com_list: Arguments passed to the vault
    :return:
    """
    for v_opt, v_arg in com_list:
        if v_opt in ("-h", "--help"):
            Instructor.main("man_vault.txt")
        else:
            print("Not recognized option '%s'. Quitting..." % v_opt)
            sys.exit(1)
