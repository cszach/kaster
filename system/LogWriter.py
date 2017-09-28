import sys
import os
import global_var
from k_date import date


# Kaster' log file manipulator
class LogWriter(object):
    origin = os.getcwd()

    @staticmethod
    def create_log_file():
        try:
            os.mkdir("/usr/share/kaster")
            os.mknod("/usr/share/kaster/log.dat")
            with open("/usr/share/kaster/log.dat", "w") as f:
                f.write("Log file created on %s." % (date(kaster.date_format)))
        except Exception as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def write_to_log(log_str):
        try:
            with open("/usr/share/kaster/log.dat", "w") as f:
                f.write(date(kaster.date_format) + log_str + "\n")
        except FileNotFoundError:
            create_log_file()
