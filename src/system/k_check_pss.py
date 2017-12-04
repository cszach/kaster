from global_var import uppercase_chars, lowercase_chars, numbers, special_chars


def k_count_occur(input_str, holder_str):
    """
    Sum of the number of occurrences of each character in holder_str in input_str
    Example:
        input_str = "4re th3se things just gr34t 2?"
        holder_str = "42"
        # -> k_count_occur(input_str, holder_str) == 3
        # We need to count the number of occurences of two characters: "4" and "2"
        # There are 2 "4" in input_str and 1 "2" in input_str
        # 2 + 1 = 3
    :param input_str: Main string
    :param holder_str: String containing the characters whose number of occurences in input_str should be sum up
    :return: Sum of number of occurrences of every character in holder_str in input_str
    """
    flag = 0
    for c in holder_str:
        flag += input_str.count(c)

    return flag


def close_score(ep, main_inp, std_inp):
    """
    Return score base on how close main_inp is to the std_inp
    std_inp is a string in the form of 'A:B', so A -> B is the range.
    If main_inp is within that range, score is 2.
    There is also another range. This range is A - ((B - A) * (ep / 100)) -> B + ((B - A) * (ep / 100)).
    If main_inp is in this range but not in A -> B, the score is 1.
    Otherwise, the score is 0.
    This aids in k_check_pss.
    :param ep: A percentage factor to determine the relative range
    :param main_inp: Main input as an integer
    :param std_inp: A string defining the range that main_inp should be in within
    :return: A score (0, 1, 2) that tells how close main_inp is to the range given by std_inp
    """
    std_inp_min = std_inp.split(":")[0]
    std_inp_max = std_inp.split(":")[1]

    if std_inp_min == std_inp_max == "":  # This means std_inp = ":", which defines nothing and allows any value
        return 2

    if std_inp_min.isdigit() and std_inp_max.isdigit():
        std_inp_min = int(std_inp_min)
        std_inp_max = int(std_inp_max)
        if std_inp_min <= main_inp <= std_inp_max:
            return 2
        else:
            len_range = std_inp_max - std_inp_min
            # Get relative range
            range_one_min = std_inp_min - (len_range * (ep / 100))
            range_one_max = std_inp_max + (len_range * (ep / 100))
            if range_one_min <= main_inp <= range_one_max:
                del len_range, range_one_min, range_one_max
                return 1
            del len_range, range_one_min, range_one_max
            return 0

    # This rest of the function is reached when either one of two sides define nothing
    if std_inp_min.isdigit():
        if main_inp >= int(std_inp_min):
            return 2

    if std_inp_max.isdigit():
        if main_inp <= int(std_inp_max):
            return 2

    return 0


def k_check_pss(pss, k_std_file_path):
    """
    Function to check if a password is strong enough compare to the given standard.
    The standard defined in the file should defines the following variables:
        - std_p_ep {real} : Define the percentage that tells if something is too few or too many
        - std_p_length {string} : Define the minimum and maximum length (>= 8)
        - std_p_upper {string] : Define the minimum and maximum number of uppercase alphabetical characters (>= 1)
        - std_p_lower {string} : Define the minimum and maximum number of lowercase alphabetical characters (>= 1)
        - std_p_num {string} : Define the minimum and maximum number of numeric characters (>= 1)
        - std_p_sym {string} : Define the minimum and maximum number of special characters (>= 1)
    If the number of alphabetical characters (std_p_upper.MIN + std_p_lower.MIN) is more than 2,
    the characters should be found on all three rows of the keyboard.
    :param pss: Password that needs to be checked
    :param k_std_file_path: A JSON-like file defining standards for a strong password
    :return: A value rating how much the password follows the standard on a scale of 10
    """
    f = open(k_std_file_path)
    f.readline()
    std_p_ep = eval(f.readline()[:-1])
    std_p_length = f.readline()[:-1]
    std_p_upper = f.readline()[:-1]
    std_p_lower = f.readline()[:-1]
    std_p_num = f.readline()[:-1]
    std_p_sym = f.readline()[:-1]
    f.close()
    del f
    flag = 0  # Initial score
    # Add scores
    flag += close_score(std_p_ep, len(pss), std_p_length)
    flag += close_score(std_p_ep, k_count_occur(pss, uppercase_chars), std_p_upper)
    flag += close_score(std_p_ep, k_count_occur(pss, lowercase_chars), std_p_lower)
    flag += close_score(std_p_ep, k_count_occur(pss, numbers), std_p_num)
    flag += close_score(std_p_ep, k_count_occur(pss, special_chars), std_p_sym)
    if int(std_p_upper.split(":")[0]) + int(std_p_lower.split(":")[0]) > 2:
        # Define variables to check how extended the alphabetical characters in the password are
        top_row = "QWERTYUIOPqwertyuiop"
        middle_row = "ASDFGHJKLasdfghjkl"
        bottom_row = "ZXCVBNMzxcvbnm"
        if k_count_occur(pss, top_row) < 1 or k_count_occur(pss, middle_row) < 1 or k_count_occur(pss, bottom_row) < 1:
            flag -= 1
        del top_row, middle_row, bottom_row
    del std_p_ep, std_p_length, std_p_upper, std_p_lower, std_p_num, std_p_sym
    return flag
