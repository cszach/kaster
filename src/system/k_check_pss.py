import os
from global_var import uppercase_chars, lowercase_chars, numbers, special_chars


def k_count_occur(input_str, holder_str):
    """
    Sum of the number of occurences of each character in holder_str in input_str
    Example:
        input_str = "4re th3se things just gr34t 2?"
        holder_str = "42"
        # -> k_count_occur(input_str, holder_str) == 3
        # We need to count the number of occurences of two characters: "4" and "2"
        # There are 2 "4" in input_str and 1 "2" in input_str
        # 2 + 1 = 3
    :param input_str: Main string
    :param holder_str: String containing the characters whose number of occurences in input_str should be sum up
    :return: Sum of number of occurences of every character in holder_str in input_str
    """
    flag = 0
    for c in holder_str:
        flag += input_str.count(c)

    return flag


def close_score(ep, main_inp, std_inp):
    std_inp_min = int(std_inp.split(":")[0])
    std_inp_max = int(std_inp.split(":")[1])
    if main_inp >= std_inp_min and main_inp <= std_inp_max:
        return 2
    len_range = std_inp_max - std_inp_min
    range_one_min = std_inp_min - (len_range * (ep / 100))
    range_one_max = std_inp_max + (len_range * (ep / 100))
    if main_inp >= range_one_min and main_inp <= range_one_max:
        del len_range, range_one_min, range_one_max
        return 1
    del len_range, range_one_min, range_one_max
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
    If the number of alphabetical characters (std_p_upper.MIN + std_p_lower.MIN) is more than 3, the characters should be found on all three rows of the keyboard.
    :param pss: Password that needs to be checked
    :param k_std_file_path: A JSON-like file defining standards for a strong password
    :return: A value rating how much the password follows the standard on a scale of 10
    """
    exec(open(k_std_file_path).read())
    flag = 0
    flag += close_score(std_p_ep, k_count_occur(pss, uppercase_chars), std_p_upper)
    flag += close_score(std_p_ep, k_count_occur(pss, lowercase_chars), std_p_lower)
    flag += close_score(std_p_ep, k_count_occur(pss, numbers), std_p_num)
    flag += close_score(std_p_ep, k_count_occur(pss, special_chars), std_p_sym)
    return flag

