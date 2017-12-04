import sys
import os
import traceback
from getpass import getpass
import fnmatch
import global_var as k_var
from LogWriter import write_to_log
import k_random
from k_check_pss import k_check_pss
from Crypto.Hash import SHA512


def check_user_account():
    """
    Check if a Kaster account is created, and if yes, check the state of the account
    Return 0 if everything is okay.
    Return -1 if no account is created.
    Return 1 if something is wrong.
    :return: An integer indicates user's account state
    """
    flag = 0
    # If no account has not yet been created, exit
    # It doesn't matter because when a new account is created,
    # all files containing credentials, key, and IVs will be deleted
    if not os.path.isfile(k_var.k_var.program_file_dir + "/0000.kas"):
        print("No account created.")
        write_to_log("pre_vault.check_user_account() : 0000.kas not found -> No account created, session abort")
        return -1

    print("Username: %s" % os.environ["SUDO_USER"])

    f_checker = open(k_var.k_var.program_file_dir + "/0000.kas", "rb")
    # Check 0000.kas file content
    first_line = f_checker.readline()
    if first_line == b"":
        flag = 1
        print("Warning: 0000.kas is empty")
        write_to_log("pre_vault.check_user_account() : Found file %s/0000.kas to be empty" % k_var.program_file_dir)
    elif first_line != bytes(os.environ["SUDO_USER"] + "\n", "utf-8"):
        flag = 1
        print("Warning: Got wrong username '%s', expected '%s'." % (os.environ["SUDO_USER"], first_line))
        write_to_log("pre_vault.check_user_account() : Username that is written in "
                     "%s/0000.kas does not seem to match with current username" % k_var.program_file_dir)
    del first_line
    if f_checker.read() == b"":
        flag = 1
        print("Warning: Couldn't find master password hash.")
        write_to_log("pre_vault.check_user_account() : Found no password hash, this is a danger")
    f_checker.close()

    # Check file containing salt
    if not os.path.isfile(k_var.k_var.program_file_dir + "/0000.salt"):
        flag = 1
        print("Warning: Couldn't find file containing master password salt.")
        write_to_log("pre_vault.check_user_account() : "
                     "Found no file containing the salt that is used for master password's hashing, this is a danger")
        print("Should clear vault's files after this operation.")
    else:
        f_checker = open(k_var.program_file_dir + "/0000.salt")
        if len(f_checker.read()) != 32:
            flag = 1
            print("Warning: Unexpected file length: File containing salt.")
            write_to_log("pre_vault.check_user_account() : "
                         "Unexpected length: %s/0000.salt, the file might have been modified" % k_var.program_file_dir)
    del f_checker

    # Check the availability of vault's files
    for file in fnmatch.filter(os.listdir(k_var.vault_file_dir), "*.dat"):
        if not os.path.isfile(k_var.vault_file_dir + "/" + file[:-4] + ".kas"):
            print("Warning: Couldn't find file containing password for login #%s" % file[:-4])
            write_to_log("pre_vault.check_user_account() : Found no file containing password for login #%s" % file[:-4])
            flag = 1
        if not os.path.isfile(k_var.vault_file_dir + "/" + file[:-4] + ".kiv"):
            print("Warning: Couldn't find file containing IV for login #%s" % file[:-4])
            write_to_log("pre_vault.check_user_account() : Found no file containing IV for login #%s" % file[:-4])
            flag = 1

    # Result
    if flag == 0:
        print("Account state: OK")
        write_to_log("pre_vault.check_user_account() : Found no problem, session end")
        del flag
        return 0
    else:
        print("Account state: NOT OK")
        write_to_log("pre_vault.check_user_account() : Found problem(s), session end")
        del flag
        return 1


def create_default_std():
    """
    Create the default file that defines Kaster's password standards
    :return:
    """
    if not os.path.isdir(k_var.std_file_dir):
        os.mkdir(k_var.std_file_dir)
    f = open(k_var.std_file_dir + "/kaster.std", "w")
    f.write("Kaster Password Standard\n")
    f.write("2 / 9 * 100\n")
    f.write("12:30\n")
    f.write("3:\n")
    f.write("3:\n")
    f.write("3:\n")
    f.write("3:\n")
    f.close()
    del f


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
            # Just having a while loop to make sure it does return a strong password
            while True:
                mst_pass = k_random.random_string("ps")
                if k_check_pss(mst_pass, k_var.std_file_dir + "/kaster.std") == 10:
                    print("Your password is: '%s'" % mst_pass)
                    print("(Exclude the single quotes around it)")
                    print("Please REMEMBER this password.")
                    input("Hit Enter to continue")
                    break
        elif getpass("Confirm password: ") == mst_pass:
            pss_score = k_check_pss(mst_pass, k_var.std_file_dir + "/kaster.std")
            if pss_score != 10:  # Compare password to Kaster's standard
                os.system("clear")
                print("Warning: Your password is not strong enough based on Kaster Password Standard (%d/10)."
                      % pss_score)
                print("You can enter nothing to get a randomly-generated password")
                del pss_score, mst_pass
                sign_up()
                return
        else:
            print("Warning: Passwords do not match. Aborting...")
            f.close()
            os.remove(k_var.program_file_dir + "/0000.kas")
            del f, mst_pass
            sys.exit(12)
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
    create_default_std()

    if not create_acc:
        return
    sign_up()
