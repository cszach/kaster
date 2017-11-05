from datetime import datetime

months_name = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def k_now(time_f, date_f):
    """
    Return the current time and date string
    :param time_f: Time format
    :param date_f: Date format
    :return:
    """
    flag = ""
    if time_f is not None:
        flag += datetime.now().strftime(time_f)
    if date_f is not None:
        flag = flag + " " + datetime.now().strftime(date_f) if time_f is not None else datetime.now().strftime(date_f)
    return flag
