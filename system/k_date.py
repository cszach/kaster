from datetime import datetime

months_name = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


# Return a date string aligned in the given format
def date(d_format):
    now = datetime.now()

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

    return "/".join(flag).upper()
