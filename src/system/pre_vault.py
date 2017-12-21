import sys
import os
from string import ascii_uppercase, ascii_lowercase, digits, punctuation
import traceback
from getpass import getpass
import fnmatch
import global_var as k_var
from LogWriter import write_to_log
import k_random
from Crypto.Hash import SHA512


def check_user_account():
    """
    Check if a Kaster account is created, and if yes, check the state of the account
    Return 0 if everything is okay.
    Return -1 if no account is created.
    Return 1 if something is wrong.
    :return: An integer indicates user's account state
    """
    __process__ = "pre_vault.check_user_account()"

    flag = 0
    # If no account has not yet been created, exit
    # It doesn't matter because when a new account is created,
    # all files containing credentials, key, and IVs will be deleted
    if not os.path.isfile(k_var.program_file_dir + "/0000.kas"):
        print("No account created.")
        write_to_log("%s : 0000.kas not found -> No account created, session abort" % __process__)
        return -1

    print("Username: %s" % os.environ["SUDO_USER"])

    c_f = open(k_var.program_file_dir + "/0000.kas", "rb")
    # Check 0000.kas file content
    grep_username = c_f.readline().decode("utf-8")[:-1]
    if grep_username == b"":
        flag = 1
        print("Warning: 0000.kas is empty")
        write_to_log("%s : Found file %s/0000.kas to be empty" % (__process__, k_var.program_file_dir))
    elif grep_username != os.environ["SUDO_USER"] and os.environ["SUDO_USER"] != "root":
        flag = 1
        print("Warning: Got wrong username '%s', expected '%s'." %
              (os.environ["SUDO_USER"], grep_username))
        write_to_log("%s : Username that is written in "
                     "%s/0000.kas does not seem to match with current username" % (__process__, k_var.program_file_dir))
    del grep_username
    if c_f.read() == b"":
        flag = 1
        print("Warning: Couldn't find master password hash.")
        write_to_log("%s : Found no password hash, this is a danger" % __process__)
    c_f.close()

    # Check file containing salt
    if not os.path.isfile(k_var.program_file_dir + "/0000.salt"):
        flag = 1
        print("Warning: Couldn't find file containing master password salt.")
        write_to_log("%s : Found no file containing the salt that is used "
                     "for master password's hashing, this is a danger" % __process__)
    else:
        c_f = open(k_var.program_file_dir + "/0000.salt")
        if len(c_f.read()) != 32:
            flag = 1
            print("Warning: Unexpected file length: File containing salt.")
            write_to_log("%s : Unexpected length: %s/0000.salt" % (__process__, k_var.program_file_dir))

    # Check the availability of vault's files
    # If they do exist, check if they are okay
    # (Like make sure IV's files are 16 in bytes length)
    f_content = None
    file_name = None
    for file in fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat"):
        file_name = file[:-4]
        if not os.path.isfile("%s/%s.kas" % (k_var.vault_file_dir, file_name)):
            flag = 1
            write_to_log("%s : Found no file containing password for login #%s" % (__process__, file[:-4]))
            print("Warning: Couldn't find file containing password for login #%s" % file[:-4])
        if not os.path.isfile("%s/%s.kiv" % (k_var.vault_file_dir, file_name)):
            flag = 1
            write_to_log("%s : Found no file containing IV for login #%s" % (__process__, file[:-4]))
            print("Warning: Couldn't find file containing IV for login #%s" % file[:-4])
        else:
            c_f = open("%s/%s.kiv" % (k_var.vault_file_dir, file_name), "rb")
            f_content = c_f.read()
            c_f.close()
            if len(f_content) != 16:
                flag = 1
                print("Warning: Unexpected file length: File containing IV for login %s. " % file[:-4])
                write_to_log("%s : Unexpected length: %s/%s.kiv" % (__process__, k_var.vault_file_dir, file[:-4]))

    del c_f, f_content, file_name

    # Result
    if flag == 0:
        print("Account state: OK")
        write_to_log("%s : Found no problem, session end" % __process__)
        del flag, __process__
        return 0
    else:
        print("Account state: NOT OK")
        write_to_log("%s : Found problem(s), session end" % __process__)
        del flag, __process__
        return 1


def sign_up():
    """
    Sign up session
    :return:
    """
    # Clear vault path
    if os.path.isdir(k_var.vault_file_dir):
        os.system("rm -rf %s" % k_var.vault_file_dir)
    os.mkdir(k_var.vault_file_dir)
    p_hash = SHA512.new()
    try:
        print("Sign Up")
        print("==============================")
        print("Username: %s" % os.environ["SUDO_USER"])
        f = open(k_var.program_file_dir + "/0000.kas", "wb")
        f.write(bytes(os.environ["SUDO_USER"] + "\n", "utf-8"))
        mst_pass = getpass("Password: ")

        if len(mst_pass) == 0:
            # If input is nothing then generate a random password as said
            # Usually k_random.random_string("ps") would return a strong-enough password
            mst_pass = k_random.random_string("ps")
            print("Your master password is: '%s'" % mst_pass)
            print("(Exclude the single quotes around it)")
            print("Remember it.")
        else:
            pass_score_flag = sum(1 for char in mst_pass if char.isalpha()) \
                              + sum(1 for char in mst_pass if char.isdigit())

            register_failed = False
            confirm_password = None
            if pass_score_flag % 9 < 9 and len(mst_pass) < 12:
                print("Warning: Your password is not strong enough.")
                register_failed = True
            else:
                confirm_password = getpass("Confirm password: ")
                if mst_pass != confirm_password:
                    print("Warning: Passwords do not match.")
                    register_failed = True

            try:
                if register_failed:
                    f.close()
                    os.remove(k_var.program_file_dir + "/0000.kas")
                    sys.exit(1)
            finally:
                del f, mst_pass, pass_score_flag, confirm_password, register_failed

        salt = k_random.random_hex(32)  # Create salt
        p_hash.update((mst_pass + salt).encode("utf-8"))  # Create hash
        f.write(p_hash.digest())  # Save hash
        f.close()
        os.system("chmod o-r %s" % (k_var.program_file_dir + "/0000.kas"))  # Make file unreadable to non-sudo privilege
        f = open(k_var.program_file_dir + "/0000.salt", "w")
        f.write(salt)  # Save salt
        del salt
        f.close()
        os.system("chmod o-r %s" % (k_var.program_file_dir + "/0000.salt"))
        del f, mst_pass
        print("New account for user %s created." % os.environ["SUDO_USER"])
        write_to_log("Created an account for %s." % os.environ["SUDO_USER"])
    except KeyboardInterrupt:
        os.remove(k_var.program_file_dir + "/0000.kas")
        if os.path.isfile(k_var.program_file_dir + "/0000.salt"):
            os.remove(k_var.program_file_dir + "/0000.salt")
        write_to_log("Quit sign up session due to keyboard interruption.")
        print("Got keyboard interruption, quitting...")
        return
    except Exception as e:
        os.remove(k_var.program_file_dir + "/0000.kas")
        if os.path.isfile(k_var.program_file_dir + "/0000.salt"):
            os.remove(k_var.program_file_dir + "/0000.salt")
        write_to_log("An error occurred during a sign up session: %s" % e)
        print("An error occurred during sign up session.")
        print("=====Traceback=====")
        traceback.print_exc()
        return


def sign_in():
    """
    Sign in session
    :return:
    """
    print("Sign In")
    print("==============================")
    print("Username: %s" % os.environ["SUDO_USER"])

    # Get password hash right away
    # No get password then get hash 'cuz that's more dangerous, perhaps?
    f = open(k_var.program_file_dir + "/0000.kas", "rb")
    f.readline()
    p_hash = f.read()
    f.close()

    # Get salt
    f = open(k_var.program_file_dir + "/0000.salt", "r")
    p_salt = f.read()
    f.close()
    del f

    input_mst_pass = getpass("Password: ")
    hash_factor = SHA512.new()
    hash_factor.update((input_mst_pass + p_salt).encode("utf-8"))
    del p_salt
    # Check if the input password hash is the same as the saved hash
    if hash_factor.digest() != p_hash:
        print("Authentication failed: Wrong password.")
        del p_hash, hash_factor
        return 1

    del p_hash, hash_factor
    return input_mst_pass


def main(create_acc):
    """
    All processes to be ran if pre_vault is called.
    :param create_acc: Boolean to tell if creating an account is required
    :return:
    """
    if not os.path.isdir(k_var.vault_file_dir):
        os.mkdir(k_var.vault_file_dir)

    if not create_acc:
        return
    sign_up()
