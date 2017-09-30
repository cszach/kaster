from datetime import datetime

months_name = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

now = datetime.now()


def date(d_format):
    """
    Return the date string, formatted by the format specified
    :param d_format: The format to be applied to the date string
    :return: The date string, formatted by d_format
    """

    f_format = d_format.upper().split("/")
    flag = []

    for i in range(len(f_format)):
        if f_format[i] == "DD":
            flag.append(now.day)
        elif f_format[i] == "MM":
            flag.append(now.month)
        elif f_format[i] == "M":
            flag.append(months_name[now.month - 1])
        elif f_format[i] == "YYYY":
            flag.append(now.year)
        elif f_format[i] == "YY":
            flag.append(now.year % 2000)
        else:
            return None  # Error

    return "/".join([str(i) for i in flag])


def time(t_format):
    """
    Return the time string, formatted by the format specified
    :param t_format: The format to be applied to the time string
    :return: The time string, formatted by t_format
    """

    t_format = t_format.upper().split(":")
    flag = []

    for i in range(len(t_format)):
        if t_format[i] == "S":
            flag.append(now.second)
        elif t_format[i] == "M":
            flag.append(now.minute)
        elif t_format[i] == "H":
            flag.append(now.hour)
        else:
            return None  # Error

    return ":".join([str(i) for i in flag])
