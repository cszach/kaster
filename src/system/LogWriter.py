import sys
import os
import global_var
from k_date import date


# Kaster' log file manipulator, deals everything that involves the log file
class LogWriter(object):
    origin = os.getcwd()

    def create_log_file(self):
        try:
            os.mkdir(global_var.program_file_dir)
            os.mknod(global_var.log_file_dir)
            with open(global_var.log_file_dir, "w") as f:
                f.write("Log file created on %s." % (date(kaster.date_format)))
        except FileExistsError:
            return
        except Exception as e:
            print(e)
            sys.exit(1)

    def write_to_log(self, log_str):
        try:
            with open(global_var.log_file_dir, "a") as f:
                f.write(date(kaster.date_format) + log_str + "\n")
        except FileNotFoundError:
            create_log_file()
