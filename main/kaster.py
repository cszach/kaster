"""
@program Kaster Password Vault
@date 28 September 2017
@author NOVAglow
"""

import sys
sys.path.insert(0, "../system")
import global_var
import pre_kaster
from Instructor import Instructor

pre_kaster.check_program_file_dir()

kasterInstructor = Instructor()

com = sys.argv[1:]
if len(com) == 0:
    kasterInstructor.print_help()
    sys.exit(0)
