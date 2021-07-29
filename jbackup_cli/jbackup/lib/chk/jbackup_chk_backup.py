#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import sys
from jbackup.lib.etc.jbackup_error import jbackup_error

# initial check python version
try:
   p = sys.version
except subprocess.CalledProcessError as e:
   print(e)
   raise SystemExit
except Exception as e:
   print(e)
   raise SystemExit
else:
   version = str(p).split(" ")[0].split(".")[0]

if(int(version) == 2):
   import os
   import os.path
   import subprocess
   import commands
elif(int(version) >= 3):
   import os
   import os.path
   import subprocess
else:
   print("Please check Python version!!!")
   raise SystemExit

from jbackup.lib.log.jbackup_logging import Logging

class jbackup_chk_backup:
### START DEF ###

   def _chk_backup(self,ver,log_file):
      rb = jbackup_error()
      try:
         if(ver >= 3):
            x = subprocess.getstatusoutput('xtrabackup --version')
         else:
            x = commands.getstatusoutput('xtrabackup --version')
      except Exception as e:
         rb.raise_err(False,1101,log_file)
      else:
         if(x[0] == 0):
            xtra_ver = x[1].split('version ')[1].split(' ')[0]
         else:
            rb.raise_err(False,1101,log_file)

         if (x[0] == 0):
            Logging._logging(log_file , "Xtabackup connection - [OK]")
            Logging._logging(log_file , "Xtabackup version - " + xtra_ver)
         else:
            rb.raise_err(False,1102,log_file)

      try:
         if(ver >= 3):
            i = subprocess.getstatusoutput('innobackupex --version')
         else:
            i = commands.getstatusoutput('innobackupex --version')
      except Exception as e:
         rb.raise_err(False,1103,log_file)
      else:
         if (i[1].split(' ')[0] == 'innobackupex'):
            inno_ver = i[1].split('version ')[1].split('-')[0]
         else:
            if ('Utility' in i[1]):
               inno_ver = i[1].split('Utility ')[1].split('-')[0][1:]
            else:
               inno_ver = i[1].split('version ')[1]
         if (i[0] == 0):
            Logging._logging(log_file , "Innobackupex connection - [OK]")
            Logging._logging(log_file , "Innobackupex version - " + inno_ver)
         else:
            rb.raise_err(False,1104,log_file)

      return xtra_ver
### END DEF ###
