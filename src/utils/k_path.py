from sys import exit
import os.path


# Get user's home directory
# If user is under root or sudo then "/root" is not what we wanted
# That's why the bash file is there to help
if not os.path.isfile("../minion/grephome.sh"):
    print("CRITICAL: Could not find grephome.sh: File missing")
    exit(1)
os.system("chmod +x ../minion/grephome.sh")
os.system("bash ../minion/grephome.sh")

userhome = open("/tmp/grephome.minion.product").read()[:-1]  # [:-1] to ignore the escape "\n"
exec(open("%s/.kasterrc" % userhome).read())

kaster_dir = program_file_dir
config_path = "%s/%s" % (userhome, ".kasterrc")
log_path = "%s/%s" % (program_file_dir, "log.dat")
man_dir = "%s/%s" % (program_file_dir, "man")
vault_dir = "%s/%s" % (program_file_dir, "vault")
