"""
system/pre_vault.py - Tasks to be done when the vault is initialized

Copyright (C) 2017-2018 Nguyen Hoang Duong <you_create@protonmail.com>
Licensed under MIT License (see LICENSE).
"""

import sys
import os
import traceback
from getpass import getpass
# import fnmatch
from Crypto.Hash import SHA512
sys.path.insert(0, "../utils")
from global_vars import *
import k_random


def check_user_account(console_output=False):
    """
    Check if a Kaster account is created, and if yes, check the state of the account
    :param console_output: Tell the function whether to write console output or not
    :return: 330 if nothing is wrong with the account
              331 if something is wrong with the account
              334 if no account is created
    """
    __process__ = "pre_vault.py -> check_user_account()"

    if not console_output:
        kaster_logger.removeHandler(o_handler)

    # If no account has not yet been created, exit
    # It doesn't matter because when a new account is created,
    # all files containing credentials, key, and IVs will be deleted
    if not os.path.isfile(kaster_dir + "/0000.kas"):
        kaster_logger.warning("%s: %s/0000.kas not found, assuming that no account is created" % (__process__, kaster_dir))
        if not console_output:
            kaster_logger.addHandler(o_handler)
        return 334

    flag = 0

    c_f = open(kaster_dir + "/0000.kas", "rb")
    # TODO: Check 0000.kas file content (contains username and master password hash)
    grep_username = c_f.readline().decode("utf-8")[:-1]
    if grep_username == b"":
        flag = 1
        kaster_logger.warning("%s: Fetched nothing for username, username empty?" % (__process__, kaster_dir))
    elif grep_username != os.environ["SUDO_USER"] and os.environ["SUDO_USER"] != "root":
        flag = 1
        kaster_logger.info("%s: Fetched username is '%s', user running Kaster as '%s' with sudo/root permission"
                           % (__process__, grep_username, os.environ["SUDO_USER"]))
        kaster_logger.warning("%s: Fetched wrong username (%s), wrong username is written to file, "
                              "or user is using a different username"
                              % (__process__, grep_username))
    del grep_username

    if c_f.read() == b"":
        flag = 1
        kaster_logger.warning("%s: Could not find master password hash" % __process__)
    c_f.close()

    # TODO: Check file containing salt
    if not os.path.isfile(kaster_dir + "/0000.salt"):
        flag = 1
        kaster_logger.warning("%s: Could not find salt for password's hashing process" % __process__)
    else:
        c_f = open(kaster_dir + "/0000.salt")
        if len(c_f.read()) != 32:
            flag = 1
            kaster_logger.warning("%s: Unexpected salt length: %s"
                                  % (__process__, kaster_dir + "/0000.salt"))

    # Check the availability of vault's files
    # If they do exist, check if they are okay
    # (Like make sure IV's files are 16 in bytes length)
    # f_content = None
    # file_name = None
    # for file in fnmatch.filter(os.listdir(vault_dir), "*.dat"):
    #     file_name = file[:-4]
    #     if not os.path.isfile("%s/%s.kas" % (vault_dir, file_name)):
    #         flag = 1
    #         write_to_log("%s : Found no file containing password for login #%s" % (__process__, file[:-4]))
    #         print("Warning: Couldn't find file containing password for login #%s" % file[:-4])
    #     if not os.path.isfile("%s/%s.kiv" % (vault_dir, file_name)):
    #         flag = 1
    #         write_to_log("%s : Found no file containing IV for login #%s" % (__process__, file[:-4]))
    #         print("Warning: Couldn't find file containing IV for login #%s" % file[:-4])
    #     else:
    #         c_f = open("%s/%s.kiv" % (vault_dir, file_name), "rb")
    #         f_content = c_f.read()
    #         c_f.close()
    #         if len(f_content) != 16:
    #             flag = 1
    #             print("Warning: Unexpected file length: File containing IV for login %s. " % file[:-4])
    #             write_to_log("%s : Unexpected length: %s/%s.kiv" % (__process__, vault_dir, file[:-4]))

    del c_f #, f_content, file_name

    flag = "OK" if flag == 0 else "NOT OK"
    return_value = 330 if flag == "OK" else 331

    if console_output:
        print("Account status: %s" % flag)
    del flag, __process__

    if not console_output:
        kaster_logger.addHandler(o_handler)

    return return_value


def sign_up():
    """
    Sign up session
    :return: 310 if operation success
              311 if registration failed due to Exception
              312 if registration failed due to register_failed = True
              313 if a keyboard interrupt signal is received
    """
    __process__ = "pre_vault.py -> sign_up()"

    # TODO: Clear vault path
    if os.path.isdir(vault_dir):
        os.system("rm -rf %s" % vault_dir)
    os.mkdir(vault_dir)
    p_hash = SHA512.new()

    try:
        # TODO: Get input for signing up
        print("Sign Up")
        print("==============================")
        print("Username: %s" % os.environ["SUDO_USER"])
        f = open(kaster_dir + "/0000.kas", "wb")
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
            register_failed = False
            r_reason = None
            confirm_password = None

            # Check if password is strong enough
            pass_score_flag = sum(1 for char in mst_pass if char.isalpha()) \
                              + sum(1 for char in mst_pass if char.isdigit())

            if pass_score_flag % 9 < 9 and len(mst_pass) < 12:
                r_reason = "Password is not strong enough"
                register_failed = True
            else:
                confirm_password = getpass("Confirm password: ")
                if mst_pass != confirm_password:
                    r_reason = "Passwords do not match"
                    register_failed = True

            try:
                if register_failed:
                    f.close()
                    os.remove(kaster_dir + "/0000.kas")
                    kaster_logger.warning("%s: Registration failed: %s" % (__process__, r_reason))
                    del f, mst_pass
                    return 312
            finally:
                del pass_score_flag, confirm_password, register_failed, r_reason

        # TODO: Create account

        # TODO: Create SHA512 hash of master password with salt as cryptographic input and save the hash in 0000.kas
        salt = k_random.random_hex(32) # Create salt
        p_hash.update((mst_pass + salt).encode("utf-8"))  # Create hash
        f.write(p_hash.digest())  # Save hash
        f.close()
        os.system("chmod o-r %s" % (kaster_dir + "/0000.kas"))  # Make file unreadable to non-sudo privilege

        # TODO: Save salt in 0000.salt
        f = open(kaster_dir + "/0000.salt", "w")
        f.write(salt)
        del salt
        f.close()
        os.system("chmod o-r %s" % (kaster_dir + "/0000.salt"))

        del f, mst_pass
        kaster_logger.info("%s: New account created for user %s" % (__process__, os.environ["SUDO_USER"]))

        return 310

    except KeyboardInterrupt:
        os.remove(kaster_dir + "/0000.kas")
        if os.path.isfile(kaster_dir + "/0000.salt"):
            os.remove(kaster_dir + "/0000.salt")
        kaster_logger.info("%s: Quit sign up session: Keyboard interrupted" % __process__)
        return 313

    except Exception as e:
        os.remove(kaster_dir + "/0000.kas")
        if os.path.isfile(kaster_dir + "/0000.salt"):
            os.remove(kaster_dir + "/0000.salt")
        kaster_logger.error("%s: An error occurred during sign up session: %s" % (__process__, e))
        print("=====Traceback=====")
        traceback.print_exc()
        return 311


def sign_in():
    """
    Sign in session
    :return: User's master password if authentication success
              321 if authentication failed due to wrong password
    """
    __process__ = "pre_vault.py -> sign_in()"

    print("Sign In")
    print("==============================")
    print("Username: %s" % os.environ["SUDO_USER"])

    # TODO: Get password hash
    f = open(kaster_dir + "/0000.kas", "rb")
    f.readline()
    p_hash = f.read()
    f.close()

    # TODO: Get salt
    f = open(kaster_dir + "/0000.salt", "r")
    p_salt = f.read()
    f.close()
    del f

    input_mst_pass = getpass("Password: ")
    hash_factor = SHA512.new()
    hash_factor.update((input_mst_pass + p_salt).encode("utf-8"))
    del p_salt

    # TODO: Check if the input password hash is the same as the saved hash
    if hash_factor.digest() != p_hash:
        kaster_logger.warning("%s: Authentication failed: Wrong password" % __process__)
        del p_hash, hash_factor
        return 321

    del p_hash, hash_factor
    return input_mst_pass


def main(create_acc):
    """
    All processes to be ran if pre_vault is called.
    :param create_acc: Boolean to tell if creating an account is required
    :return:
    """
    if not os.path.isdir(vault_dir):
        os.mkdir(vault_dir)

    if not create_acc:
        return
    sign_up()
