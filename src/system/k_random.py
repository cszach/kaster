from global_var import *
from random import choice, randint


def random_string(*args):
    """
    Generate and return a random string

    Modes:
        ns : Not specified
        ps : Password
        pn : PIN

    random_string(mode):
        mode : |ns|ps|pn|
            ns: Not specified -> Return a random string with a length between 1 and 30.
            ps: Password -> Return a random string. Length 12 to 30. Can contain printable ASCII.
            pn: PIN -> Return a random string. Length from 2 to 12. Can only contain ASCII numbers.

    random_string(mode, length)
        mode : |ps|pn|
        length: length of the string to be returned

    random_string(length, a1, a2, a3, a4)
        length: Length of the string to be returned
        a1: A boolean to tell whether uppercase English characters are allowed or not. True if yes.
        a2: A boolean to tell whether lowercase English characters are allowed or not. True if yes.
        a3: A boolean to tell whether numbers from 0 to 9 are allowed or not. True if yes.
        a4: A boolean to tell whether special characters are allowed or not. True if yes.

    random_string(mode, length, a1, a2, a3, a4)
        mode: |ps|
        length: Length of the string to be returned
        a1, a2, a3, a4: Reference above

    :param args: Arguments to be passed as input for random string generation
    :return: Randomly generated string, processed with the arguments
    """
    if args[0] == "ns":  # Not specified
        return random_string(randint(1, 30), True, True, True, True)

    if args[0] == "ps":
        # Create password
        if len(args) == 1:
            return random_string(randint(12, 30), True, True, True, True)
        if len(args) == 2:
            return random_string(args[1], True, True, True, True)  # Take args[1] as length
        if len(args) == 6:
            return random_string(args[1], args[2], args[3], args[4], args[5])

    if args[0] == "pn":
        if len(args) == 1:
            return random_string(randint(2, 12), None, None, True, None)
        if len(args) == 2:
            return random_string(args[1], None, None, True, None)

    allowed_chars = ""  # A string that holds the characters that can be presented in the output string

    if args[1]:
        allowed_chars += uppercase_chars
    if args[2]:
        allowed_chars += lowercase_chars
    if args[3]:
        allowed_chars += numbers
    if args[4]:
        allowed_chars += special_chars

    if args[0] is None:
        pss_length = randint(12, 30)
    else:
        pss_length = args[0]

    if args[1] == args[2] == args[3] == args[4] == (False or None):
        allowed_chars = uppercase_chars + lowercase_chars + numbers + special_chars

    return "".join([choice(allowed_chars) for _ in range(pss_length)])


def random_hex(length):
    """
    Generate and return a random hexadecimal number
    :param length: Number of digits in the output hexadecimal
    :return: A randomly generated hexadecimal number with [length] digits
    Example: random_hex(7) returns a hexadecimal number with 7 digits
    """
    return "".join([choice(numbers + lowercase_chars[:6]) for _ in range(length)])
