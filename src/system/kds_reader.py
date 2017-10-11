import sys
import os


def kds_reader(kds_file):
    """
    Reader for Kaster Defined Standard file (.kds)
    Kaster Defined Standard files are files that define the "standard" of something (i.e. password, system config)
    From there, the tester can rate a given object based on the "standard" given
    :param kds_file:
    :return:
    """
    if os.path.isfile(kds_file):  # Check for file's existance
        f = open(kds_file, "r")
        f.close()
    else:
        print("Error: No Kaster Defined Standard (.kds) file found")
        sys.exit(1)
