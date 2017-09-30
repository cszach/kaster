import sys
from random import randint
sys.path.insert(0, "../system")
import k_random
from LogWriter import LogWriter


log_writer = LogWriter()


def generator(arguments):
    """
    Session for generating string
    :param arguments: Arguments to be passed to the generator
    :return:
    """
    if arguments[0] in ["pw", "ps", "password"]:  # Generate password
        """
        Setup
        
        runner : current index
        p_length : password length (string)
        p_x : number of output passwords (string)
        p_uuc : use uppercase characters (boolean)
        p_ulc : use lowercase characters (boolean)
        p_un : use numbers (boolean)
        p_us : use symbols (boolean)
        write_to_log : write to log file the output (boolean)
        
        """
        runner = 1
        p_length = None
        p_x = 1
        p_uuc = p_ulc = p_un = p_us = None
        write_to_log = False

        # TODO: Scan arguments
        while runner < len(arguments):
            if arguments[runner] == "-l":
                try:
                    p_length = int(arguments[runner + 1])
                    runner += 1
                except ValueError:
                    log = "Error: Invalid value for password's length."
                    print(log)
                    log_writer.write_to_log(log)
                    del log
                    sys.exit(1)
            elif arguments[runner] == "-d":
                try:
                    p_x = int(arguments[runner + 1])
                    runner += 1
                except ValueError:
                    log = "Error: Invalid value for number of passwords."
                    print(log)
                    log_writer.write_to_log(log)
                    del log
                    sys.exit(1)
            elif arguments[runner] == "-u":
                p_uuc = True
            elif arguments[runner] == "-l":
                p_ulc = True
            elif arguments[runner] == "-n":
                p_un = True
            elif arguments[runner] == "-s":
                p_us = True
            elif arguments[runner] == "--write-to-log":
                write_to_log = True
            else:
                log = "Error: Unknown argument \"%s\"." % (arguments[runner])
                print(log)
                log_writer.write_to_log(log)
                del log
                sys.exit(1)
            runner += 1

        # TODO: Generate password(s) and print them as output
        if p_length is None:
            flag = True
        else:
            flag = False

        for i in range(p_x):
            if flag:
                p_length = randint(12, 30)
            output = k_random.random_string(p_length, p_uuc, p_ulc, p_un, p_us)
            print("Output [%d] %s" % (i + 1, output))
            if write_to_log:
                log_writer.write_to_log(output)

        del output, flag
        del p_length, p_x, p_uuc, p_ulc, p_un, p_us, write_to_log

    if arguments[0] in ["pn", "pin"]:  # Generate PIN
        """
        Setup
        
        runner : current index
        p_length : number of digits to be presented
        p_x : number of output PINs
        """
        runner = 1
        p_length = randint(2, 12)
        p_x = 1
        write_to_log = False

        # TODO: Scan arguments
        while runner < len(arguments):
            if arguments[runner] == "-l":
                p_length = arguments[runner + 1]
                runner += 1
            elif arguments[runner] == "-d":
                p_x = arguments[runner + 1]
                runner += 1
            elif arguments[runner] == "--write-to-log":
                write_to_log = True
            else:
                log = "Error: Unknown argument \"%s\"." % (arguments[runner])
                print(log)
                log_writer.write_to_log(log)
                del log
                sys.exit(1)
            runner += 1

        # TODO: Generate and output PINs
        for i in range(p_x):
            output = k_random.random_string("pn", p_length)
            print("Output [%d] %s" % (i + 1, output))
            if write_to_log:
                log_writer.write_to_log(output)

        del output
        del runner, p_length, p_x, write_to_log
