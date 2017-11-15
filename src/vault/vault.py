import sys
import os
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
    if len(com_list) == 0:
        Instructor.main("man_vault.txt")
        sys.exit(0)
    pre_vault.main(False)
    for v_opt, v_arg in com_list:
        if v_opt in ("-h", "--help"):
            Instructor.main("man_vault.txt")
        elif v_opt == "--account":
            print("In session: pre_vault.check_user_account()...")
            result = pre_vault.check_user_account()
            print("pre_vault.check_user_account() session ended.")
            if result == -1:
                if input("No account created, create one now? [Y|N] ").lower() == "y":
                    pre_vault.main(True)
                else:
                    sys.exit(0)
        else:
            print("Not recognized option '%s'. Quitting..." % v_opt)
            sys.exit(1)
