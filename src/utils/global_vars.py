"""
utils/global_vars.py - Variables that are used by Kaster and Kaster subprograms

Copyright (C) 2017-2018 Nguyen Hoang Duong <novakglow@gmail.com>
Licensed under MIT License (see LICENSE).
"""

from sys import exit
import os.path
import logging

__process__ = "global_vars.py"

# TODO: Get user's home directory
# If user is under root or sudo then "/root" is not what we wanted
# That's why the bash file is there to help
if os.getenv("SUDO_USER") is None:
    print("Please run Kaster as root")
    exit(409)

if not os.path.isfile("minion/grephome.sh"):
    print("CRITICAL::%s: Could not find grephome.sh (minion/grephome.sh): File missing" % __process__)
    exit(401)

# TODO: Execute grephome.sh minion process, which leaves out a file containing the user's home directory path in it
os.system("chmod +x minion/grephome.sh")
os.system("bash minion/grephome.sh")

try:
    userhome = open("/tmp/grephome.minion.product").read()[:-1]  # [:-1] to ignore the escape "\n"
except FileNotFoundError as e:
    print("FATAL::%s: Could not fetch /tmp/grephome.minion.product: %s" % (__process__, e))
    print("Check file integrity of minion.grephome.sh")
    exit(402)

# TODO: Get settings in .kasterrc
try:
    exec(open("%s/.kasterrc" % userhome).read())
except FileNotFoundError:
    print("FATAL::%s: Could not find Kaster's configuration file (.kasterrc) in home directory" % __process__)
    print("Make sure that you've ran install.sh.")
    exit(403)

# TODO: Assign variables for use
kaster_dir = program_file_dir
config_path = "%s/%s" % (userhome, ".kasterrc")
log_path = "%s/%s" % (program_file_dir, "log.dat")
man_dir = "%s/%s" % (program_file_dir, "man")
vault_dir = "%s/%s" % (program_file_dir, "vault")
time_fm = time_format
date_fm = date_format

# TODO: Setup logger

kaster_logger = logging.getLogger("Kaster global logger")
kaster_logger.setLevel(logging.DEBUG)

# File handler for logger
f_handler = logging.FileHandler(log_path)
f_handler.setLevel(logging.INFO)
fmter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", time_fm + " " + date_fm)
f_handler.setFormatter(fmter)
kaster_logger.addHandler(f_handler)
del f_handler, fmter

# Output stream handler for logger
o_handler = logging.StreamHandler()
o_handler.setLevel(logging.WARNING)
fmter = logging.Formatter("%(levelname)s: %(message)s", time_fm + " " + date_fm)
o_handler.setFormatter(fmter)
kaster_logger.addHandler(o_handler)
