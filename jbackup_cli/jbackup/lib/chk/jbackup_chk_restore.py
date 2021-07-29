#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import os
import os.path
import sys
import subprocess
import re
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_chk_restore:
### START DEF ###
      def _get_restore_dir(self, file, log_file):
         rb = jbackup_error()
         info = []
         chk_file = jbackup_chk_dir(log_file)
         if (chk_file._exist_file(file)):
            cnf_file = file
         else:
            print("Check cnf file in restore DB server!!!")
            raise SystemExit

         keep_phrases = ["datadir"]

         with open(cnf_file) as f:
            f = f.readlines()

         for line in f:
            for phrase in keep_phrases:
               if re.match(phrase, line):
                  info.append(line)
                  break
         try:
            restore_dir = info[0].split('=')[1].split('\n')[0]
         except Exception as err:
            rb.raise_err(True,3011, log_file)
         else:
            return restore_dir.replace(" ","")

### END DEF ###
