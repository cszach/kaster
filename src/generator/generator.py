"""
generator/generator.py - Password generator subprogram for Kaster
This subprogram used k_random.random_string() as core (see utils/k_random.py)

Copyright (C) 2017-2018 Nguyen Hoang Duong <novakglow@gmail.com>
Licensed under MIT License (see LICENSE).
"""

import sys
import os
sys.path.insert(0, "../system")
import Instructor
sys.path.insert(0, "../utils")
from global_vars import *
from k_random import random_string


def generator(com_list):
    """
    Session for generating string
    :param com_list: Arguments to be passed to the generator
    :return: 700 if operation success
              701 if there's no option (len(com_list) == 0)
              702 if only -h or --help is passed as argument
              703 if there's unrecognized option
              704 if user abort file operation when prompted to overwrite or append output file
    """
    __process__ = "generator.py -> generator()"

    # If no option is specified for the generator, generate a random password
    if len(com_list) == 0:
        generator([("--duplicate", "1")])
        return 701

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
    p_length = None
    p_duplicate = 1
    p_use_upper = None
    p_use_lower = None
    p_use_number = None
    p_use_symbol = None
    output_file_name = None
    kaster_logger.debug("%s: Done variable setup for password generation" % __process__)

    number_of_warnings = 0

    # TODO: Get options
    for g_opt, g_arg in com_list:
        if g_opt in ("-h", "--help"):
            Instructor.main("man_gen.txt")
            # If that is the only option, exit right away so that the generator won't create a password
            if len(com_list) == 1:
                del p_length, p_duplicate, p_use_upper, p_use_lower, p_use_number, p_use_symbol, output_file_name
                return 702

        elif g_opt in ("-l", "--length"):
            try:
                p_length = int(g_arg)
                if p_length > 30 or p_length < 8:
                    kaster_logger.warning("WARNING::%s: Invalid password's length (%d): Must be between 8 and 30.\n"
                                          "  A random value in between 12 and 30 will be used instead."
                                          % (__process__, p_length))
                    number_of_warnings += 1
                    p_length = None
            except ValueError:
                kaster_logger.warning("WARNING::%s: Invalid value for password's length (%s).\n"
                                      "  A random value in between 12 and 30 will be used instead."
                                      % (__process__, g_arg))
                number_of_warnings += 1
                p_length = None

        elif g_opt in ("-d", "--duplicate"):
            try:
                p_duplicate = int(g_arg)
                if p_duplicate < 1:
                    kaster_logger.warning("WARNING::%s: Invalid value for duplication (%d): Must be greater than 0.\n"
                                          "  1 is used instead."
                                          % (__process__, p_duplicate))
                    number_of_warnings += 1
                    p_duplicate = 1
            except ValueError:
                kaster_logger.warning("WARNING::%s: Invalid value for duplication (%s).\n"
                                      "  1 is used instead."
                                      % (__process__, g_arg))
                number_of_warnings += 1
                p_duplicate = 1

        elif g_opt in ("-o", "--output"):
            if not os.path.isfile(g_arg):
                output_file_name = g_arg
            else:
                kaster_logging.warning("LIGHT WARNING::%s: File '%s' has already existed." % (__process__, g_arg))
                u_choice = input("Do you want to append or overwrite the file? Or abort operation? [A|O|C] ")
                try:
                    if u_choice.lower() == "o":  # Overwrite -> Remove the file and create a new one with the same name
                        os.remove(g_arg)
                        open(g_arg, "a").close()
                        output_file_name = g_arg
                    elif u_choice.lower() == "c":  # Cancel
                        return 704
                    elif u_choice.lower() != "a":  # Invalid option
                        output_file_name = None  # Assigning to None means no record
                        kaster_logger.warning("WARNING::%s: Unrecognized option (%s)\n"
                                              "  There will be no output to file."
                                              % (__process__, u_choice))
                        number_of_warnings += 1
                        continue
                    else:  # That means user chooses "a" -> Append
                        output_file_name = g_arg
                finally:
                    del u_choice

        elif g_opt == "--upper":
            p_use_upper = True
        elif g_opt == "--lower":
            p_use_lower = True
        elif g_opt == "--number":
            p_use_number = True
        elif g_opt == "--symbol":
            p_use_symbol = True

        else:
            # ???: Should we just ignore unrecognized option?
            kaster_logger.error("ERROR::%s: Not recognized option (%s)" % (__process__, g_opt))
            return 703

    # TODO: Prepare file if an output file name is specified
    f = None
    if output_file_name is not None:
        try:
            f = open(output_file_name, "a")
        except FileNotFoundError:
            # We say no parent folder because, the user might input a path with directories in it,
            # and while open() can create a file in case a file with specified file name does not exist,
            # it cannot create new directories.
            kaster_logger.warning("WARNING::%s: Parent folder of %s does not exist"
                                  "  There will be no output to file."
                                  % (__process__, output_file_name))
            number_of_warnings += 1
            output_file_name = None

    if number_of_warnings > 0:
        print("\n===== * =====\n")

    # TODO: Generate password(s) and write output
    g_output = None
    for i in range(p_duplicate):
        g_output = random_string(p_length, p_use_upper, p_use_lower, p_use_number, p_use_symbol)
        print(g_output)
        if output_file_name is not None:
            f.write(g_output + "\n")

    if output_file_name is not None:
        f.close()

    if number_of_warnings > 0:
        print("\n===== * =====")
        print("Total number of warnings: %d")
        print("Scroll up to see them.")

    del p_length, p_duplicate, p_use_upper, p_use_lower, p_use_number, p_use_symbol
    del g_output, f, output_file_name, number_of_warnings

    return 700
