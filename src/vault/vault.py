import sys
import os
import traceback
from getpass import getpass
sys.path.insert(0, "../system")
import global_var
import LogWriter
import pre_vault
import Instructor


def clear_vault_dir():
    """
    Clear vault's folder (/usr/share/kaster/vault).
    :return:
    """
    os.system("rm -rf /usr/share/kaster/vault")
    os.mkdir(global_var.program_file_dir + "/vault")


def mediate_check_account():
    """
    A function to mediate session pre_vault.check_user_account().
    Base on the returned value, the program can make further decisions.
    :return: pre_vault.check_user_account()
    """
    LogWriter.write_to_log("Start session: pre_vault.check_user_account()")
    print("In session: pre_vault.check_user_account()...")
    try:
        result = pre_vault.check_user_account()
    except Exception as e:
        LogWriter.write_to_log("Failed session: pre_vault.check_user_account() with exception: %s" % e)
        print("Session encountered an error: pre_vault.check_user_account()")
        print("Full traceback")
        traceback.print_exc()
        sys.exit(1)
    print("Finish session: pre_vault.check_user_account()...")
    LogWriter.write_to_log("End session: pre_vault.check_user_account()")
    return result


def new_login_ui():
    """
    Interface: Create new login
    :return:
    """
    login_name = None
    login = None
    password = None
    note = None
    print("New login")
    login_name = input("Login name: ")
    login = input("Login: ")
    password = getpass("Password: ")
    note = input("Note/Comment (you can hit enter if there's nothing): ")


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
    for v_idx, (v_opt, v_arg) in enumerate(com_list):
        if v_opt in ("-h", "--help"):
            Instructor.main("man_vault.txt")
        elif v_opt == "--account":
            if mediate_check_account() == -1:
                if input("No account created, create one now? [Y|N] ").lower() == "y":
                    pre_vault.main(True)
                else:
                    sys.exit(0)
        elif v_opt == "--new":
            if mediate_check_account() == -1:
                print("No account created. Use './kaster.py --vault --account' to create one.")
                sys.exit(0)
            if mediate_check_account() == 1:
                print("Warning: Found problem(s) during pre_vault.check_user_account() session, "
                      "resolve them and try again")
                sys.exit(0)
            if pre_vault.sign_in() != 0:
                sys.exit(1)
            if com_list[v_idx + 1:] == 0:
                LogWriter.write_to_log("Start session: vault > new_login_ui()")
                print("In session: new_login_ui()")
                try:
                    new_login_ui()
                except Exception as e:
                    LogWriter.write_to_log("Failed session: vault > new_login_ui() with exception: %s" % e)
                    print("Session encountered an error: new_login_ui()")
                    print("Full traceback")
                    traceback.print_exc()
                    sys.exit(1)
                LogWriter.write_to_log("End session: vault > new_login_ui()")
                print("Finish session: new_login_ui()")
        else:
            print("Not recognized option '%s'. Quitting..." % v_opt)
            sys.exit(1)
