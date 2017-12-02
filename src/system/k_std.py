from os.path import isfile
from global_var import std_file_dir
from LogWriter import write_to_log


def to_word(line):
    """
    A function to aid in read_std().
    :param line: A line from a .std file
    :return:
    """
    s_min = line.split(":")[0]
    s_max = line.split(":")[1]
    if s_min.isdigit() and s_max.isdigit():
        return "in between %s and %s." % (s_min, s_max)
    if s_min.isdigit():
        return "at least %s." % s_min
    if s_max.isdigit():
        return "at most %s." % s_max
    return "can be anything."


def read_std(std_file_name):
    """
    Print out the content of the standard defined in a .std file.
    :param std_file_name: The name of the .std file
    :return:
    """
    f = open(std_file_dir + "/" + std_file_name, "r")
    print("The %s defines the following rules for password to be considered \"strong\":" % f.readline())
    ep = eval(f.readline())
    print("Length: %s" % to_word(f.readline()))
    print("Number of uppercase characters: %s" % to_word(f.readline()))
    print("Number of lowercase characters: %s" % to_word(f.readline()))
    print("Number of numerical characters: %s" % to_word(f.readline()))
    print("Number of special characters: %s" % to_word(f.readline()))
    if ep == 0:
        print("All of the above rules must be strictly followed under this standard.")
    else:
        print("For factors that have a range (a minimum value and a maximum value),")
        print("this standard allows them to be about %f%% off the range." % format(ep, ".2f"))


def check_std(std_file_name):
    """
    Check if a .std file (a file containing rules for a strong password, defined by a password standard) is okay.
    :param std_file_name: The name of the .std file
    :return: An integer. 0 if the file is okay, 1 if it is not, -1 if it does not exist.
    """
    write_to_log("Start session: k_std.check_std()")
    print("In session: k_std.check_std()")
    if not isfile(std_file_dir + "/" + std_file_name):
        write_to_log("k_std.check_std() : File does not exist: %s" % (std_file_dir + "/" + std_file_name))
        print("File does not exist, quitting...")
        write_to_log("End session: k_std.check_std()")
        print("Finish session: k_std.check_std()")
        return -1
    number_of_lines = sum(1 for _ in open(std_file_dir + "/" + std_file_name))
    if number_of_lines != 7:
        write_to_log("k_std.check_std() : Got unexpected number of lines in the file [%s]" % std_file_name)
        print("Warning: Unexpected number of lines %s, expected 7" % number_of_lines)
        write_to_log("End session: k_std.check_std()")
        print("Finish session: k_std.check_std()")
        return 1
    result = 0
    f = open(std_file_dir + "/" + std_file_name, "r")
    f.readline()
    flag = None
    try:
        flag = eval(f.readline())
    except SyntaxError:
        result = 1
        write_to_log("k_std.check_std() : Cannot evaluate expression at line 2")
        print("Warning: Cannot evaluate expression at line 2, which is used to get the second range")
    for i in range(5):
        flag = f.readline()
        if (not flag.split(":")[0].isdigit() and flag.split(":")[0] != "") or \
                (not flag.split(":")[1].isdigit() and flag.split(":")[1] != "") or (flag.count(":") != 1):
            result = 1
            write_to_log("k_std.check_std() : Invalid rule: %s" % flag)
            continue
    f.close()
    del f, flag
    return result
