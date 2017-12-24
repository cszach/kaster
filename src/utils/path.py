from sys import exit
import os.path


def userhome():
    """
    Get (normal) user's home directory. Under sudo/root does not return '/root'
    :return: User's home directory
    """
    if not os.path.isfile("../minion/grephome.sh"):
        print("CRITICAL: Could not find grephome.sh: File missing")
        exit(1)
    os.system("chmod +x ../minion/grephome.sh")
    os.system("bash ../minion/grephome.sh")
    return open("/tmp/grephome.minion.product").read()[:-1]


exec(open("%s/.kasterrc" % userhome()).read())
kaster_dir = program_file_dir
config_path = "%s/%s" % (userhome(), ".kasterrc")
log_path = "%s/%s" % (program_file_dir, "log.dat")
man_f_dir = "%s/%s" % (program_file_dir, "man")
vault_f_dir = "%s/%s" % (program_file_dir, "vault")
