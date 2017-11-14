import sys
import os
from getpass import getpass
import fnmatch
from global_var import *
import LogWriter
import k_random
from k_check_pss import k_check_pss
from Crypto.Hash import SHA512


def check_user_account():
    """
    Check if the user account exists.
    If it does, return 0.
    If it does not but there are files that save logins, return -1.
    Otherwise, return 1.
    :return: An indicator integer
    """
    if os.path.isfile(program_file_dir + "/0000.kas") \
            and os.path.isfile(program_file_dir + "/0000.salt"):  # Basically checks if master password has been created
        return 0
    if not os.path.isdir(vault_file_dir) \
            or not os.path.isfile(vault_file_dir + "/0000.kas") or not os.path.isfile(program_file_dir + "/0000.salt"):
        return 1
    if len(fnmatch.filter(os.listdir(vault_file_dir), "*.kas")) > 1:
        return -1


def account_state():
    """
    Check account state
    :return: 0 if everything is okay overall, 1 if something is NOT okay
    """
    print("In session: pre_vault.account_state()")
    flag = 0
    for i in range(1, 10000):
        if os.path.isfile(vault_file_dir + "{0:04}".format(i) + ".dat"):
            if not os.path.isfile(vault_file_dir + "{0:04}".format(i) + ".kas"):
                print("Warning: Password not found for login #%s" % ("{0:04}".format(i)))
                flag = 1
            if not os.path.isfile(vault_file_dir + "{0:04}".format(i) + ".kiv"):
                print("Warning: IV not found for login #%s" % ("{0:04}".format(i)))
                flag = 1
    return flag


def create_default_std():
    """
    Create the default file that defines Kaster's password standards
    :return:
    """
    if not os.path.isdir(std_file_dir):
        os.mkdir(std_file_dir)
    f = open(std_file_dir + "/kaster.std", "w")
    f.write("2 / 9 * 100\n")
    f.write("12:30\n")
    f.write("2:4\n")
    f.write("2:4\n")
    f.write("2:4\n")
    f.write("2:4\n")
    f.close()
    del f


def sign_up():
    """
    Sign up session
    :return:
    """
    mst_pass = None
    p_hash = SHA512.new()
    try:
        print("Sign Up")
        print("==============================")
        print("Username: %s" % os.environ["SUDO_USER"])
        f = open(program_file_dir + "/0000.kas", "wb")
        f.write(bytes(os.environ["SUDO_USER"] + "\n", "utf-8"))
        mst_pass = getpass("Password: ")
        if len(mst_pass) == 0:
            # If input is nothing then generate a random password as said
            # Usually k_random.random_string("ps") would return a strong-enough password
            # Just having a while loop to make sure it does return a strong password
            while True:
                mst_pass = k_random.random_string("ps")
                if k_check_pss(mst_pass, std_file_dir + "/kaster.std") == 10:
                    print("Your password is: '%s'" % mst_pass)
                    print("(Exclude the single quotes around it)")
                    print("Please REMEMBER this password.")
                    input("Hit Enter to continue")
                    break
        elif getpass("Confirm password: ") == mst_pass:
            if k_check_pss(mst_pass, std_file_dir + "/kaster.std") != 10:
                os.system("clear")
                print("Warning: Your password is not strong enough based on Kaster Password Standard.")
                print("You can enter nothing to get a randomly-generated password")
                sign_up()
                return
        else:
            print("Warning: Passwords do not match. Aborting...")
            f.close()
            os.remove(program_file_dir + "/0000.kas")
            del f, mst_pass
            sys.exit(12)
        salt = k_random.random_hex(32)
        p_hash.update((mst_pass + salt).encode("utf-8"))
        f.write(p_hash.digest())
        f.close()
        f = open(program_file_dir + "/0000.salt", "w")
        f.write(salt)
        del salt
        f.close()
        del f, mst_pass
        print("New account for user %s created." % os.environ["SUDO_USER"])
        LogWriter.write_to_log("Created an account for %s." % os.environ["SUDO_USER"])
    except (KeyboardInterrupt, Exception):
        os.remove(program_file_dir + "/0000.kas")
        if os.path.isfile(program_file_dir + "/0000.salt"):
            os.remove(program_file_dir + "/0000.salt")
        return


def main(create_acc):
    """
    All processes to be ran if pre_vault is called.
    :param create_acc: Boolean to tell if creating an account is required
    :return:
    """
    if not os.path.isdir(std_file_dir):
        os.mkdir(std_file_dir)
    if not os.path.isdir(vault_file_dir):
        os.mkdir(vault_file_dir)
    create_default_std()
    # Check if master.kas exists
    # If it does not, it highly means the user hasn't created an account yet
    if not create_acc:
        return
    if check_user_account() == 1:
        # Clear vault folder
        # Just in case the user fucks up the files
        os.system("rm -rf %s" % vault_file_dir)
        os.mkdir(vault_file_dir)
        # Start sign up session
        sign_up()
    elif check_user_account() == -1:
        print("Warning: Master password is not found but files that save login credentials/passwords were found")
        if input("Do you want to clear them? (You should) [Y|N]") == "Y":
            os.system("rm -rf %s" % vault_file_dir)
        sign_up()
