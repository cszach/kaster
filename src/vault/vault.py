import sys
import os
from getpass import getpass
sys.path.insert(0, "../system")
import global_var
import pre_vault
import Instructor


def clear_vault_dir():
    """
    Clear vault's folder (/usr/share/kaster/vault).
    :return:
    """
    os.system("rm -rf /usr/share/kaster/vault")
    os.mkdir(global_var.program_file_dir + "/vault")


def vault(com_list):
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
