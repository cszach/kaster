from sys import exit
import os.path


# Get user's home directory
# If user is under root or sudo then "/root" is not what we wanted
# That's why the bash file is there to help
if os.getenv("SUDO_USER") is None:
    print("Please run Kaster as root")
    exit(1)

if not os.path.isfile("minion/grephome.sh"):
    print("CRITICAL: Could not find grephome.sh (minion/grephome.sh): File missing")
    exit(1)

os.system("chmod +x minion/grephome.sh")
os.system("bash minion/grephome.sh")

try:
    userhome = open("/tmp/grephome.minion.product").read()[:-1]  # [:-1] to ignore the escape "\n"
except FileNotFoundError as e:
    print("FATAL: Could not fetch /tmp/grephome.minion.product: %s" % e)
    print("Check file integrity of minion.grephome.sh")
    exit(1)

try:
    exec(open("%s/.kasterrc" % userhome).read())
except FileNotFoundError:
    print("FATAL: Could not find Kaster's configuration file (.kasterrc) in home directory")
    print("Make sure that you've ran install.sh.")
    exit(1)

kaster_dir = program_file_dir
config_path = "%s/%s" % (userhome, ".kasterrc")
log_path = "%s/%s" % (program_file_dir, "log.dat")
man_dir = "%s/%s" % (program_file_dir, "man")
vault_dir = "%s/%s" % (program_file_dir, "vault")
time_fm = time_format
date_fm = date_format
enable_mst_pw = enable_mst_pw

# Logger setup
kaster_logger = logging.getLogger("Kaster global logger")
kaster_logger.setLevel(logging.INFO)
fmter = logging.Formatter("%(levelname)s: %(message)s", time_fm + " " + date_fm)
handler.setFormatter(fmter)

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
kaster_logger.addHandler(o_handler)
