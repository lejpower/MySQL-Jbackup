# -*- coding: utf-8 -*-
import sys
import shutil
import subprocess
import os.path
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_run_binary:
   def _exec_backup(self, binlog_list , binlog_backup_dir, log_file):
      rb = jbackup_error()
      #############################################
      if (len(binlog_list) != 0):
         for l in binlog_list:
            try:
               shutil.copy(l,binlog_backup_dir)
            except Exception as err:
               rb.raise_err(True,1032, log_file)
            else:
               Logging._logging(log_file, "[Copied] " + str(l) + " to " + str(binlog_backup_dir))
               return_code = 0
      else:
          Logging._logging(log_file, "There are not target binary-log files")
          Logging._logging(log_file, "Please check binary-log directory or cnf file!")
          return_code = 0

      return return_code
