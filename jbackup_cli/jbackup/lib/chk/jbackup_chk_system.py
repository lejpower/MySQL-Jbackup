#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os.path
import sys
import multiprocessing
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_chk_system:
### START DEF ###

   # disk size check
   def __init__(self, tmp_log_file):
      self.log_file = tmp_log_file
      self.rb = jbackup_error()

   def _cpu_chk(self):
      try:
         cnt = multiprocessing.cpu_count()
      except Exception as err:
         self.rb.raise_err(True,2001, self.log_file)
         ##Logging._logging(self.log_file, "Can not get CPU information")
         ##raise SystemExit
      else:
         return cnt

   def _get_para_opt(self):
      try:
         cnt = multiprocessing.cpu_count()
         if (cnt == 1):
            para = 1
         elif (cnt == 2):
            para = 1
         elif (cnt > 2):
            para = cnt / 2
      except Exception as err:
         self.rb.raise_err(True,2002, self.log_file)
         ##Logging._logging(self.log_file, "Can not calculate CPU count")
         ##raise SystemExit
      else:
         return int(para)

   def _python_ver(self):
      try:
         self.p = sys.version
         py_ver = str(self.p).split(" ")[0].split(".")[0]
      except subprocess.CalledProcessError as err:
         self.rb.raise_err(True,2003, self.log_file)
         ##Logging._logging(self.log_file, "Can not get Python version")
         ##raise SystemExit
      except Exception as err:
         self.rb.raise_err(True,2003, self.log_file)
         ##Logging._logging(self.log_file, "Can not calculate CPU count")
         ##raise SystemExit
      else:
         return int(py_ver)

   # python version check
   def _python_logging(self):
      py_ver = str(self.p).split(" ")[0]

      if (int(py_ver.split(".")[0]) < 3):
         Logging._logging(self.log_file, "Python version - " + str(py_ver))
         Logging._logging(self.log_file,"Please check Python version. it is not new version!")
      else:
         Logging._logging(self.log_file, "Python version - " + str(py_ver) + " [OK]")


### END DEF ###
