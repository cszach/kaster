import sys
import os
import traceback
from random import randint
from getpass import getpass
import fnmatch
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import pyperclip
sys.path.insert(0, "../system")
import global_var as k_var
from LogWriter import write_to_log
import pre_vault
from k_random import random_string
import Instructor


def clear_vault_dir():
    """
    Clear vault's folder.
    :return:
    """
    os.system("rm -rf /usr/share/kaster/vault")
    os.mkdir(k_var.program_file_dir + "/vault")


def mediate_check_account():
    """
    A function to mediate session pre_vault.check_user_account().
    Base on the returned value, the program can make further decisions.
    :return: pre_vault.check_user_account()
    """
    write_to_log("Start session: pre_vault.check_user_account()")
    print("In session: pre_vault.check_user_account()...")
    try:
        result = pre_vault.check_user_account()
    except Exception as e:
        write_to_log("Failed session: pre_vault.check_user_account() with exception: %s" % e)
        print("Session encountered an error: pre_vault.check_user_account()")
        print("Full traceback")
        traceback.print_exc()
        sys.exit(1)
    print("Finish session: pre_vault.check_user_account()...")
    write_to_log("End session: pre_vault.check_user_account()")
    return result


def pre_action():
    """
    An operation which alert the user if there's no Kaster account
    or there's a problem with their account (files missing, invalid files,...).
    Typically put before performing a password manager action (like --new, --get, ...)
    :return:
    """
    check_result = mediate_check_account()
    if check_result == -1:
        print("No account created. Use './kaster.py --vault --account' to create one.")
        del check_result
        sys.exit(0)
    if check_result == 1:
        print("Warning: Found problem(s) during pre_vault.check_user_account() session, "
              "resolve them and try again")
        del check_result
        sys.exit(1)
    del check_result
    print()


def key(inp_pass):
    """
    Create key for password encrypting.
    This is mostly used with the user's master password passed in, to create key
    for a login's password encryption. No need to store key in a file.
    The same password outputs the same key.
    :param inp_pass: Password as input
    :return: Key
    """
    # Get salt
    f = open(k_var.program_file_dir + "/0000.salt", "r")
    salt = f.read()
    f.close()
    del f

    # Create hash
    f_hash = SHA256.new()
    f_hash.update((inp_pass + salt).encode("utf-8"))
    del salt
    return f_hash.digest()


def new_login_ui(master_password, login_id):
    """
    Interface: Create new login
    :param master_password: Master password as input
    :param login_id: Login's ID, pre-generated to serve keyboard interruption catching
    :return:
    """
    print("New login")
    login_name = input("Login name: ")
    if login_name == "":
        print("Input empty, assigning login name to login's ID: %s" % login_id)
        login_name = login_id

    login = input("Login: ")
    if login == "":
        print("Input empty, assigning login to username: %s" % os.environ["SUDO_USER"])
        login = os.environ["SUDO_USER"]

    password = getpass("Password (leave blank to generate one): ")
    if password == "":
        password = random_string("ps")
    note = input("Note/Comment (leave blank if there's nothing): ")

    # Save login name, login, and comment
    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "w")
    f.write(login_name + "\n")
    f.write(login + "\n")
    f.write(note + "\n")
    f.close()

    # Create IV and save it
    iv = os.urandom(16)
    f = open("%s/%s.kiv" % (k_var.vault_file_dir, login_id), "wb")
    f.write(iv)
    f.close()

    # Save encrypted password
    flag = AES.new(key(master_password), AES.MODE_CFB, iv)
    del iv
    f = open("%s/%s.kas" % (k_var.vault_file_dir, login_id), "wb")
    f.write(flag.encrypt(password))
    del flag, password
    f.close()
    del f


def get_login(login_id):
    """
    Get login credentials based on login's ID
    :param login_id: Target login's ID
    :return:
    """
    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "r")
    print(f.readline()[:-1])  # Print login name
    print("====================")
    print("Login: %s" % f.readline()[:-1])
    print("ID: %s" % login_id)
    comment = f.readline()[:-1]
    f.close()
    del f
    if comment != "":
        print("Comment: %s" % comment)
    del comment


def get_id_from_arg(arg):
    """
    Turn argument arg to integer if possible, else terminate the program.
    Created to get ID without rewriting a try-catch block over and over.
    :param arg: ID string (user's input)
    :return:
    """
    try:
        return "%04d" % int(arg)
    except ValueError:  # Get this when arg contains non-numerical character(s)
        print("Error: Invalid ID string")
        sys.exit(1)


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
            pre_action()
            if len(fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat")) == 9999:
                print("Warning: Cannot save a new login, try deleting an existed login")
                sys.exit(1)
            master = pre_vault.sign_in()
            if master == 1:
                del master
                sys.exit(1)  # Login failed
            if len(com_list[v_idx + 1:]) == 0:  # No further argument -> Login UI
                write_to_log("Start session: vault > new_login_ui()")
                print()
                print("In session: new_login_ui()")
                login_id = None
                try:
                    # Create ID
                    # Make sure the ID login is not a duplicate
                    while True:
                        login_id = "%04d" % randint(1, 9999)
                        if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, login_id)):
                            break
                    new_login_ui(master, login_id)
                    del master, login_id
                except KeyboardInterrupt:
                    del master
                    if login_id is None:
                        del login_id
                        sys.exit(0)
                    # On keyboard interrupt, revert all actions to avoid any mistake next time
                    if os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.dat" % (k_var.vault_file_dir, login_id))
                    if os.path.isfile("%s/%s.kas" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.kas" % (k_var.vault_file_dir, login_id))
                    if os.path.isfile("%s/%s.kiv" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.kiv" % (k_var.vault_file_dir, login_id))
                    del login_id
                    print("Got keyboard interruption, quitting...")
                    sys.exit(0)
                except Exception as e:
                    del master, login_id
                    # On error, revert all actions to avoid any mistake next time
                    if os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.dat" % (k_var.vault_file_dir, login_id))
                    if os.path.isfile("%s/%s.kas" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.kas" % (k_var.vault_file_dir, login_id))
                    if os.path.isfile("%s/%s.kiv" % (k_var.vault_file_dir, login_id)):
                        os.remove("%s/%s.kiv" % (k_var.vault_file_dir, login_id))
                    write_to_log("Failed session: vault > new_login_ui() with exception: %s" % e)
                    print("Session encountered an error: new_login_ui()")
                    print("=====Traceback=====")
                    traceback.print_exc()
                    sys.exit(1)
                write_to_log("End session: vault > new_login_ui()")
                print("Finish session: new_login_ui()")
            else:  # User specifies additional arguments, so process them
                login_name = None
                login = None
                password = None
                note = None
                for login_opt, login_arg in com_list[v_idx + 1:]:
                    if login_opt == "--name":
                        login_name = login_arg
                    elif login_opt == "--login":
                        login = login_arg
                    elif login_opt == "--password":
                        password = login_arg
                    elif login_opt == "--comment":
                        note = login_arg
                    else:
                        print("Fatal: Invalid option %s" % login_opt)
                        del master
                        del login_name, login, password, note
                        sys.exit(1)

                # Create ID such that it is not a duplicate
                while True:
                    login_id = "%04d" % randint(1, 9999)
                    if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, login_id)):
                        break

                # Process collected results to make sure every variable is assigned to a valid value
                if login_name is None or login_name == "":
                    print("Input for login name is empty, assigning login name to login's ID: %s" % login_id)
                    login_name = login_id
                if login is None or login == "":
                    print("Input for login is empty, assigning login to username: %s" % os.environ["SUDO_USER"])
                    login = os.environ["SUDO_USER"]
                if password is None or password == "":
                    print("Input for password is empty, assigning to a random password...")
                    password = random_string("ps")
                if note is None:
                    note = ""

                # Save login name, login, and comment
                f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "wb")
                f.write(bytes(login_name + "\n", "utf-8"))
                f.write(bytes(login + "\n", "utf-8"))
                f.write(bytes(note + "\n", "utf-8"))
                f.close()
                del login_name, login, note

                # Create IV and save it
                iv = os.urandom(16)
                f = open("%s/%s.kiv" % (k_var.vault_file_dir, login_id), "wb")
                f.write(iv)
                f.close()

                # Save encrypted password
                flag = AES.new(key(master), AES.MODE_CFB, iv)
                del master, iv
                f = open("%s/%s.kas" % (k_var.vault_file_dir, login_id), "wb")
                f.write(flag.encrypt(password))
                del password, flag
                f.close()
                del f
            write_to_log("New login created")
            print("New login created.")
            sys.exit(0)
        elif v_opt == "--list":
            pre_action()
            # Check if there is any .dat file (file containing login credentials except password
            if len(fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat")) == 0:
                print("No login to list.")
            else:
                login_name = None
                login_id = None
                print("ID   |Login name")
                print("=====|==========")
                for k_login_f in fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat"):
                    f = open("%s/%s" % (k_var.vault_file_dir, k_login_f), "rb")
                    login_name = f.readline()[:-1].decode("utf-8")
                    f.close()
                    login_id = k_login_f[:-4]
                    print("%s | %s" % (login_id, login_name))
                del login_name, login_id
        elif v_opt == "--get":
            pre_action()
            get_id = get_id_from_arg(v_arg)
            if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, get_id)):
                print("Login does not exist.")
                del get_id
                sys.exit(1)
            get_login(get_id)
            del get_id
        elif v_opt == "--getpass":
            pre_action()
            master = pre_vault.sign_in()
            if master == 1:
                del master
                sys.exit(1)  # Login failed

            get_id = get_id_from_arg(v_arg)
            if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, get_id)):
                print("Login does not exist.")
                del get_id
                sys.exit(1)

            # Get IV
            f = open("%s/%s.kiv" % (k_var.vault_file_dir, get_id), "rb")
            iv = f.read()
            f.close()
            # Get encrypted password
            f = open("%s/%s.kas" % (k_var.vault_file_dir, get_id), "rb")
            pss = f.read()
            f.close()
            del f

            # Decrypt password
            flag = AES.new(key(master), AES.MODE_CFB, iv)
            del iv, master
            pss = flag.decrypt(pss)
            del flag
            try:
                pyperclip.copy(pss.decode("utf-8"))  # Copy password to clipboard
                print("Password for login #%s copied." % get_id)
            except UnicodeDecodeError as e:
                del pss, get_id
                write_to_log("An error occurred while decoding the password: %s" % e)
                print("Error: Could not decode password: In format UTF-8")
                sys.exit(1)
            del pss, get_id
        elif v_opt == "--edit":
            pre_action()
            master = pre_vault.sign_in()
            if master == 1:
                del master
                sys.exit(1)  # Login failed
            if len(com_list[v_idx + 1:]) == 0:
                print("Warning: Must specify more options")
                print("Type './kaster.py --vault --help' for the manual page")
                sys.exit(1)
            login_id = "%04d" % int(v_arg)
            if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, login_id)):
                write_to_log("User attempts to edit a login but Kaster couldn't find it")
                print("Error: Could not find login #%s" % login_id)
                del login_id
                sys.exit(1)
            for edit_opt, new_value in com_list[v_idx + 1:]:
                if edit_opt == "--name":
                    flag = new_value
                    if new_value == "":
                        print("Empty input for new login name, assigning it to login's ID: %s" % login_id)
                        flag = login_id
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "rb")
                    f.readline()
                    rest = f.read()
                    f.close()
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "wb")
                    f.write(bytes(flag + "\n", "utf-8"))
                    del flag
                    f.write(rest)
                    del rest
                    f.close()
                    del f
                elif edit_opt == "--login":
                    flag = new_value
                    if new_value == "":
                        print("Empty input for new login, assigning it to username %s" % os.environ["SUDO_USER"])
                        flag = os.environ["SUDO_USER"]
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "rb")
                    mediate_a = f.readline()
                    f.readline()
                    rest = f.read()
                    f.close()
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "wb")
                    f.write(mediate_a)
                    del mediate_a
                    f.write(bytes(flag + "\n", "utf-8"))
                    del flag
                    f.write(rest)
                    del rest
                    f.close()
                    del f
                elif edit_opt == "--password":
                    flag = new_value
                    if new_value == "":
                        print("Empty input for new password, assigning it to a random one...")
                        flag = random_string("ps")
                    os.remove("%s/%s.kas" % (k_var.vault_file_dir, login_id))
                    os.remove("%s/%s.kiv" % (k_var.vault_file_dir, login_id))

                    # IV
                    iv = os.urandom(16)
                    f = open("%s/%s.kiv" % (k_var.vault_file_dir, login_id), "wb")
                    f.write(iv)
                    f.close()

                    # Save (encrypted) password
                    enc_object = AES.new(key(master), AES.MODE_CFB, iv)
                    del iv
                    f = open("%s/%s.kas" % (k_var.vault_file_dir, login_id), "wb")
                    f.write(enc_object.encrypt(flag))
                    del enc_object, flag
                    f.close()
                    del f
                elif edit_opt == "--comment":
                    flag = new_value
                    if new_value == "":
                        print("Empty input for comment, ignoring...")
                        continue
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "rb")
                    flag_a = f.readline()
                    flag_b = f.readline()
                    f.close()
                    f = open("%s/%s.dat" % (k_var.vault_file_dir, login_id), "wb")
                    f.write(flag_a)
                    del flag_a
                    f.write(flag_b)
                    del flag_b
                    f.write(bytes(flag + "\n", "utf-8"))
                    del flag
                    f.close()
                    del f
                else:
                    print("Error: Invalid option %s, aborting..." % edit_opt)
                    sys.exit(1)
            del master
            print("Data updated")
            write_to_log("Edited login #%s" % login_id)
            del login_id
            sys.exit(0)
        elif v_opt == "--del":
            get_id = get_id_from_arg(v_arg)
            if not os.path.isfile("%s/%s.dat" % (k_var.vault_file_dir, get_id)):  # If the login does not exist :/
                write_to_log("User attempts to delete a login but Kaster couldn't find it")
                print("Couldn't find login associated with ID #%s" % get_id)
                del get_id
                sys.exit(1)
            master = pre_vault.sign_in()
            if master == 1:
                del master
                sys.exit(1)  # Login failed
            del master

            flag_exitcode = 0
            if input("Are you really sure you want to delete login #%s? [Y|N] " % get_id).lower() == "y":
                try:
                    os.remove("%s/%s.dat" % (k_var.vault_file_dir, get_id))
                    os.remove("%s/%s.kas" % (k_var.vault_file_dir, get_id))
                    os.remove("%s/%s.kiv" % (k_var.vault_file_dir, get_id))
                    write_to_log("Removed login #%s" % get_id)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    write_to_log("An error occurred while deleting login #%s: %s" % (get_id, e))
                    print("An error occurred while deleting login #%s." % get_id)
                    print("=====Traceback=====")
                    traceback.print_exc()
                    flag_exitcode = 1
                finally:
                    del get_id
                    sys.exit(flag_exitcode)
            else:
                print("Aborting...")
        elif v_opt == "--delall":
            if len(fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat")) == 0:
                print("No saved login.")
                sys.exit(0)

            master = pre_vault.sign_in()
            if master == 1:
                del master
                sys.exit(1)  # Login failed
            del master

            if input("Are you really sure you want to delete all saved logins? [Y|N] ").lower() == "y":
                clear_vault_dir()
                write_to_log("Removed all saved logins")
            else:
                print("Aborting...")
        else:
            print("Fatal: Not recognized option '%s'." % v_opt)
            sys.exit(1)
