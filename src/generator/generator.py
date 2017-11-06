"""
Password generator
Not to be confused with the generator in the password vault,
this generator only generates passwords.
It does not generate IV, key, pseudorandom number or anything else.
This generator generates passwords mainly by calling k_random (found in the 'system' folder)
"""

import sys
import os
sys.path.insert(0, "../system")
from random import randint
import k_random
import Instructor


def generator(com_list):
    """
    Session for generating string
    :param com_list: Arguments to be passed to the generator
    :return:
    """
    if len(com_list) == 0:
        Instructor.main("man_gen.txt")
        sys.exit(0)

    """
    Setup variable
    p_length         : Length of output password(s).
                       If it is None, p_length will be a random value
                       between 12 and 30 (inclusive) for every iteration.
    p_duplicate      : Number of output passwords. Set to 1 by default.
    p_use_upper,
    p_use_lower,
    p_use_number,
    p_use_symbol     : Booleans to tell the generator to use uppercase characters,
                       lowercase characters, numbers, and letters or not, respectively.
                       True if it must use. False otherwise.
                       However, if all of them are set to False or None, they will all
                       be turned to True.
    output_file_name : The name for the output file (string).
    """
    # Get options and arguments
    p_length = None
    p_duplicate = 1
    p_use_upper = None
    p_use_lower = None
    p_use_number = None
    p_use_symbol = None
    output_file_name = None

    for g_opt, g_arg in com_list:
        if g_opt == "--pss":
            break  # Break and generate a random password real quick
        elif g_opt in ("-l", "--length"):
            try:
                p_length = int(g_arg)
            except ValueError:
                print("Error: Invalid value for password's length '%s'. Quitting..." % g_arg)
                sys.exit(1)
        elif g_opt in ("-d", "--duplicate"):
            try:
                p_duplicate = int(g_arg)
            except ValueError:
                print("Error: Invalid value for number of passwords '%s'. Quitting..." % g_arg)
                sys.exit(1)
        elif g_opt in ("-o", "--output"):
            if not os.path.isfile(g_arg):  # If the file does not exist
                output_file_name = g_arg
            else:
                print("File '%s' has already existed." % g_arg)
                u_choice = input("Do you want to append or overwrite the file? Or abort operation? [A|O|C] ")
                if u_choice.lower() == "o":
                    os.remove(g_arg)
                    open(g_arg, "a").close()
                    output_file_name = g_arg
                    del u_choice
                elif u_choice.lower() == "c":
                    del u_choice
                    sys.exit(8)
                elif u_choice.lower() != "a":
                    output_file_name = None
                    print("Warning: Unrecognized option '%s'. Option is ignored." % u_choice)
                    del u_choice
                    continue
                else:
                    output_file_name = g_arg
        elif g_opt == "--upper":
            p_use_upper = True
        elif g_opt == "--lower":
            p_use_lower = True
        elif g_opt == "--number":
            p_use_number = True
        elif g_opt == "--symbol":
            p_use_symbol = True
        else:
            print("Error: Not recognized option '%s'. Quitting..." % g_opt)
            sys.exit(1)

    # Generate password session

    # Check if the length for output password(s) is specified
    # If not, have flag_rl to tell the generate to have the password's length random every time
    flag_rl = None
    if p_length is None:
        flag_rl = True

    # Preparing file
    f = None
    if output_file_name is not None:
        f = open(output_file_name, "a")

    # Output
    for i in range(p_duplicate):
        if flag_rl:
            p_length = randint(12, 30)
        g_output = k_random.random_string(p_length, p_use_upper, p_use_lower, p_use_number, p_use_symbol)
        print("Output [%d] %s" %
              (i + 1, g_output))
        if output_file_name is not None:
            f.write(g_output + "\n")

    if output_file_name is not None:
        f.close()
    del p_length, p_duplicate, p_use_upper, p_use_lower, p_use_number, p_use_symbol
    del flag_rl, g_output, f, output_file_name
