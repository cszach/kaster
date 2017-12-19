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
from global_var import std_file_dir
import k_random
import Instructor


def generator_std(input_std_filename, input_options):
    """
    Session for generating passwords under a standard
    :param input_std_filename: Filename of file containing the rules of a password standard
    :param input_options: Options & Values
    :return:
    """
    save_output = None
    duplication = 1

    for gstder_opt, gstder_arg in input_options:
        if gstder_opt in ("-o", "--output"):
            save_output = gstder_arg
        elif gstder_opt in ("-d", "--duplicate"):
            try:
                duplication = int(gstder_arg)
                if duplication < 1:
                    print("Warning: Invalid value for duplication (%d). Must be greater than 0." % gstder_arg)
                    print("Assigning p_duplicate to 1...")
                    duplication = 1
            except ValueError:
                print("Error: Invalid value for number of passwords '%s'." % gstder_arg)
                sys.exit(1)
    f = None
    if save_output is not None:
        f = open(save_output, "w")

    for i in range(duplication):
        g_password = k_random.random_pass(input_std_filename)
        print("Output [%d] %s" % (i + 1, g_password))
        if save_output is not None:
            f.write(g_password + "\n")
    if save_output is not None:
        f.close()
    del i, f, g_password


def generator(com_list):
    """
    Session for generating string
    :param com_list: Arguments to be passed to the generator
    :return:
    """
    # If no option is specified for the generator, generate a random password
    if len(com_list) == 0:
        generator([("--duplicate", "1")])
        return

    if not os.path.isdir(std_file_dir):
        os.mkdir(std_file_dir)

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

    # Quick check
    got_std = False
    got_c_arg = False
    for g_opt, g_arg in com_list:
        if g_opt == "--std":
            if got_c_arg:
                print("Error: --std is specified incorrectly")
                del got_std, got_c_arg
                sys.exit(1)
            got_std = True
        elif got_std:
            print("Error: --std is specified incorrectly")
            del got_std, got_c_arg
            sys.exit(1)
        elif g_opt in ["-l", "--length", "-d", "--duplicate", "-o", "--output"]:
            got_c_arg = True
    del got_std, got_c_arg

    for g_opt, g_arg in com_list:
        if g_opt in ("-h", "--help"):
            Instructor.main("man_gen.txt")
            # If that is the only option, exit right away to avoid creating a password
            if len(com_list) == 1:
                sys.exit(0)
        elif g_opt == "--std":
            generator_std(g_arg, com_list)
            sys.exit(0)
        elif g_opt in ("-l", "--length"):
            try:
                p_length = int(g_arg)
                if p_length > 30 or p_length < 12:
                    print("Warning: Invalid password's length (%d). Must be in between 12 and 30." % p_length)
                    print("Assigning p_length to None...")
                    p_length = None
            except ValueError:
                print("Error: Invalid value for password's length '%s'." % g_arg)
                sys.exit(1)
        elif g_opt in ("-d", "--duplicate"):
            try:
                p_duplicate = int(g_arg)
                if p_duplicate < 1:
                    print("Warning: Invalid value for duplication (%d). Must be greater than 0." % p_duplicate)
                    print("Assigning p_duplicate to 1...")
                    p_duplicate = 1
            except ValueError:
                print("Error: Invalid value for number of passwords '%s'." % g_arg)
                sys.exit(1)
        elif g_opt in ("-o", "--output"):
            if not os.path.isfile(g_arg):  # If the file does not exist
                output_file_name = g_arg
            else:
                print("File '%s' has already existed." % g_arg)
                u_choice = input("Do you want to append or overwrite the file? Or abort operation? [A|O|C] ")
                if u_choice.lower() == "o":  # Overwrite -> Remove the file and create a new one with the same name
                    os.remove(g_arg)
                    open(g_arg, "a").close()
                    output_file_name = g_arg
                    del u_choice
                elif u_choice.lower() == "c":  # Cancel
                    del u_choice
                    sys.exit(8)
                elif u_choice.lower() != "a":  # Invalid option
                    output_file_name = None  # Assigning to None means no record
                    print("Warning: Unrecognized option '%s'. Option is ignored." % u_choice)
                    del u_choice
                    continue
                else:  # Append
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
            print("Fatal: Not recognized option '%s'." % g_opt)
            sys.exit(1)

    # Generate password session

    # Prepare file if an output file name is specified
    f = None
    if output_file_name is not None:
        f = open(output_file_name, "a")

    # Output
    g_output = None
    for i in range(p_duplicate):
        g_output = k_random.random_string(p_length, p_use_upper, p_use_lower, p_use_number, p_use_symbol)
        print("Output [%d] %s" %
              (i + 1, g_output))
        if output_file_name is not None:
            f.write(g_output + "\n")

    if output_file_name is not None:
        f.close()

    # Delete variables, save RAM!
    del p_length, p_duplicate, p_use_upper, p_use_lower, p_use_number, p_use_symbol
    del g_output, f, output_file_name
