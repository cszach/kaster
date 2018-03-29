import sys
import os
sys.path.insert(0, "../system")
import Instructor
sys.path.insert(0, "../utils")
from global_vars import *
import k_random


def generator(com_list):
    """
    Session for generating string
    :param com_list: Arguments to be passed to the generator
    :return:
    """
    __process__ = "generator.py (generator())"

    # If no option is specified for the generator, generate a random password
    if len(com_list) == 0:
        generator([("--duplicate", "1")])
        return

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
    kaster_logger.debug("%s: All variables required for password generation are set to None" % __process__)

    number_of_warnings = 0

    for g_opt, g_arg in com_list:
        if g_opt in ("-h", "--help"):
            Instructor.main("man_gen.txt")
            # If that is the only option, exit right away to avoid creating a password
            if len(com_list) == 1:
                sys.exit(0)
        elif g_opt in ("-l", "--length"):
            try:
                p_length = int(g_arg)
                if p_length > 30 or p_length < 12:
                    kaster_logger.warning("WARNING:%s: Invalid password's length (%d): Must be between 12 and 30"
                                    % (__process__, p_length))
                    number_of_warnings += 1
                    kaster_logger.info("INFO:%s: Assigning p_length to None" % __process__)
                    p_length = None
            except ValueError:
                kaster_logger.warning("WARNING:%s: Invalid value for password's length (%s)"
                                % (__process__, g_arg))
                number_of_warnings += 1
                kaster_logger.info("INFO:%s: Assigning p_length to None")
                p_length = None
        elif g_opt in ("-d", "--duplicate"):
            try:
                p_duplicate = int(g_arg)
                if p_duplicate < 1:
                    kaster_logger.warning("WARNING:%s: Invalid value for duplication (%d): Must be greater than 0"
                                    % (__process__, p_duplicate))
                    number_of_warnings += 1
                    kaster_logger.info("INFO:%s: Assigning p_duplicate to 1" % __process__)
                    p_duplicate = 1
            except ValueError:
                kaster_logger.warning("WARNING:%s: Invalid value for duplication (%s)"
                                % (__process__, g_arg))
                number_of_warnings += 1
                kaster_logger.info("INFO:%s: Assigning p_duplicate to 1" % __process__)
                p_duplicate = 1
        elif g_opt in ("-o", "--output"):
            if not os.path.isfile(g_arg):  # If the file does not exist
                output_file_name = g_arg
            else:
                print("File '%s' has already existed." % g_arg)
                u_choice = input("Do you want to append or overwrite the file? Or abort operation? [A|O|C] ")
                try:
                    if u_choice.lower() == "o":  # Overwrite -> Remove the file and create a new one with the same name
                        os.remove(g_arg)
                        open(g_arg, "a").close()
                        output_file_name = g_arg
                    elif u_choice.lower() == "c":  # Cancel
                        sys.exit(8)
                    elif u_choice.lower() != "a":  # Invalid option
                        output_file_name = None  # Assigning to None means no record
                        kaster_logger.warning("WARNING:%s: Unrecognized option (%s)" % (__process__, u_choice))
                        number_of_warnings += 1
                        kaster_logger.info("INFO:%s: There will be no output to file" % __process__)
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
            kaster_logger.error("FATAL:%s: Not recognized option (%s)" % (__process__, g_opt))
            sys.exit(1)

    # Generate password session

    # Prepare file if an output file name is specified
    f = None
    if output_file_name is not None:
        try:
            f = open(output_file_name, "a")
        except FileNotFoundError:
            kaster_logger.warning("WARNING:%s: Parent folder of %s does not exist" % (__process__, output_file_name))
            number_of_warnings += 1
            kaster_logger.info("INFO:%s: There will be no output to file" % __process__)
            output_file_name = None

    if number_of_warnings > 0:
        print()
        print("===== * =====")

    # Output
    g_output = None
    for i in range(p_duplicate):
        g_output = k_random.random_string(p_length, p_use_upper, p_use_lower, p_use_number, p_use_symbol)
        print("Output [%d] %s" %
              (i + 1, g_output))
        if output_file_name is not None:
            f.write(g_output + "\n")

    del p_length, p_duplicate, p_use_upper, p_use_lower, p_use_number, p_use_symbol
    del g_output

    if output_file_name is not None:
        f.close()

    del f, output_file_name

    if number_of_warnings > 0:
        print()
        kaster_logger.info("INFO:%s: Total number of warnings: %d"
                     % (__process__, number_of_warnings))
        print("Scroll up to see them.")

    del number_of_warnings
