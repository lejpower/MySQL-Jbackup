# -*- coding: utf-8 -*-

import sys
import subprocess

# initial check python version
try:
   p = sys.version
except subprocess.CalledProcessError as e:
   print(e)
   sys.exit(1)
except Exception as e:
   print(e)
   sys.exit(1)
else:
   version = str(p).split(" ")[0].split(".")[0]

if(int(version) == 2):
   import os
   import os.path
   import ConfigParser
elif(int(version) >= 3):
   import os
   import os.path
   import configparser
else:
   print("Please check Python version!!!")
   sys.exit(1)

from jbackup.lib.etc.jbackup_init import jbackup_init
from jbackup.lib.chk.jbackup_chk_option import jbackup_chk_option

from ._version import __version__

def cli_main(argv=sys.argv[1:]):

   # Check Option
   if(len(argv) == 0):
      chk_opt = jbackup_chk_option()
      chk_opt._chk_err()
      sys.exit(1)
   elif (argv[0] in ['--version','-v']):
      print(__version__)
      sys.exit(0)
   elif(argv[0] in ['help']):
      chk_opt = jbackup_chk_option()
      chk_opt._print_help()
      sys.exit(0)
   else:
      init = jbackup_init(argv)
      init_flag = 1
      check_argv = []
      init._init_process(init_flag, check_argv)

# Main
if __name__ == '__main__':
   cli_main()
