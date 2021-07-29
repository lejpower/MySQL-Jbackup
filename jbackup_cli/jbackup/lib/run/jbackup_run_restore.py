#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import sys
import subprocess
import os.path
import shutil
import glob
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.chk.jbackup_chk_dir import jbackup_chk_dir
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_run_restore:
### START DEF ###
   def _exec_restore(self, cl_user , cl_password, cl_hostname, cl_port, cnf_file, restore_dir, log_file):
      ###
      rb = jbackup_error()
      try:
         exec_cmd = "innobackupex"
         exec_cmd = exec_cmd + " --defaults-file=" + cnf_file
         exec_cmd = exec_cmd + " --host=" + cl_hostname
         exec_cmd = exec_cmd + " --port=" + cl_port
         exec_cmd = exec_cmd + " --user=" + cl_user
         exec_cmd = exec_cmd + " --password=" + cl_password
         exec_cmd = exec_cmd + " --copy-back "
         exec_cmd = exec_cmd + restore_dir

         p = subprocess.Popen(exec_cmd , shell=True, stderr=subprocess.PIPE)
      except subprocess.CalledProcessError as err:
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001, log_file)
      except Exception as err:
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001, log_file)
      else:
         while True:
            t = p.stderr.readline()
            out = t.decode('utf-8')
            if out == '' and p.poll() != None:
               break
            if out != '':
               Logging._logging(log_file, out)

      if ( p.returncode == 0):
         Logging._logging(log_file, "restore - [OK]")
      else:
         Logging._logging(log_file, "restore - [ERROR]")
         rb.raise_err(True,3008, log_file)

#####
   def _chk_exist_old_files(self, dir, log_file):
      chk_dir = jbackup_chk_dir()
      target = []

      #dir check
      if ( os.path.exists(dir) != True ):
         Logging._logging(log_file, "Nothing target directory!")
         rb.raise_err(True,1025, log_file)

      #target directory
      try:
         os.chdir(dir)
      except Exception as e:
         Logging._logging(log_file, "cannot change directory : " + dir)
         rb.raise_err(True,3005, log_file)
      else:
         if (len(glob.glob('*')) == 0):
            Logging._logging(log_file,"Nothing * file!")
         else:
            for elem in glob.glob('*'):
               if ( os.path.exists(elem) == True ):
                  target_file = os.getcwd() + '/' + elem
                  if (chk_dir._exist_dir(target_file)):
                     self._remove_dir(target_file, log_file)
                  else:
                     self._remove_file(target_file, log_file)

      #sub directory
         tmp = []
         for elem in os.listdir(dir):
            if (os.stat(elem)[3] == 2):
               tmp.append(os.path.join(dir,elem))

         for elem in tmp:
            try:
               os.chdir(elem)
            except Exception as e:
               Logging._logging(log_file, "cannot change directory : " + dir)
               rb.raise_err(True,3005, log_file)
            else:
               if (len(glob.glob('*')) == 0):
                  Logging._logging(log_file,"Nothing * file! - " + str(elem))
               else:
                  for elem in glob.glob('*'):
                     if ( os.path.exists(elem) == True ):
                        target_file = os.getcwd() + '/' + elem
                        self._remove_file(target_file, log_file)


   def _remove_file(self, arg, log_file):
      try:
         os.remove(arg)
      except Exception as e:
         Logging._logging(log_file, "Can not remove * file - " + arg)
      else:
         Logging._logging(log_file, "removed * file - " + arg)

   def _remove_dir(self, arg, log_file):
      try:
         shutil.rmtree(arg)
      except Exception as e:
         Logging._logging(log_file, "Can not remove * directory - " + arg)
      else:
         Logging._logging(log_file, "removed * directory - " + arg)

###################################

### END DEF ###
