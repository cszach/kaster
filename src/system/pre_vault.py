import sys
import os
from getpass import getpass
import hashlib
from global_var import program_file_dir
import k_random
from k_check_pss import k_check_pss


def create_default_std():
    """
    Create the default file that defines Kaster's password standards
    :return:
    """
    if not os.path.isdir(program_file_dir + "/std"):
        os.mkdir(program_file_dir + "/std")
    f = open(program_file_dir + "/std/kaster.std", "w")
    f.write("std_p_ep = 2 / 9 * 100\n")
    f.write("std_p_length = 12:30\n")
    f.write("std_p_upper = 2:4\n")
    f.write("std_p_lower = 2:4\n")
    f.write("std_p_num = 2:4\n")
    f.write("std_p_sym = 2:4\n")
    f.close()
    del f


def hash_pss(input_pss):
    """
    A method to created hash master password.
    :param input_pss: The master password
    :return:
    """
    f = open(program_file_dir + "/master.kas", "w")
    f.write(hashlib.sha512(input_pss + k_random.random_hex(64)).hexdigest())
    f.close()
    del f


def sign_up():
    """
    Sign up session
    :return:
    """
    mst_pass = None
    try:
        print("Sign Up")
        print("==============================")
        print("Username: %s" % os.getlogin())
        mst_pass = getpass("Password: ")
        if len(mst_pass) == 0:
            while True:
                mst_pass = k_random.random_string("ps")
                if k_check_pss(mst_pass, program_file_dir + "/std/kaster.std") == 10:
                    print("Your password is: '%s'" % mst_pass)
                    print("(Exclude the single quotes around it)")
                    print("Please REMEMBER this password.")
                    input("Hit Enter to continue")
                    break
            hash_pss(mst_pass)
        elif getpass("Confirm password: ") == mst_pass:
            if k_check_pss(mst_pass, program_file_dir + "/std/kaster.std") != 10:
                os.system("clear")
                print("Warning: Your password is not strong enough based on Kaster Password Standard.")
                print("You can enter nothing to get a randomly-generated password")
                sign_up()
                return
            hash_pss(mst_pass)
        else:
            print("Warning: Passwords do not match. Aborting...")
            del mst_pass
            sys.exit(12)
        del mst_pass
        print("New account for user %s created." % os.getlogin())
    except KeyboardInterrupt:
        del mst_pass
        return


def main():
    """
    All processes to be ran upon vault's call
    :return:
    """
    create_default_std()
    # Check if master.kas exists
    # If it does not, it highly means the user hasn't created an account yet
    if not os.path.isfile(program_file_dir + "/master.kas"):
        # Clear vault folder
        # Just in case the user fucks up the files
        os.system("rm -rf /usr/share/kaster/vault")
        os.mkdir(program_file_dir + "/vault")
        # Start sign up session
        sign_up()
