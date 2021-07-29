#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################

import sys
import subprocess
import glob
import os.path
from jbackup.lib.log.jbackup_logging import Logging
from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_run_applylog:
### START DEF ###
   def _exec_applylog(self, backup_user , backup_password, local_port, cnf_file, applylog_dir, log_file):
      rb = jbackup_error()
      try:
         exec_cmd = "innobackupex"
         exec_cmd = exec_cmd + " --apply-log "
         exec_cmd = exec_cmd + applylog_dir

         p = subprocess.Popen(exec_cmd , shell=True, stderr=subprocess.PIPE)
      except subprocess.CalledProcessError as err:
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001)
      except Exception as err:
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001)
      else:
         while True:
            t = p.stderr.readline()
            out = t.decode('utf-8')
            if out == '' and p.poll() != None:
               break
            if out != '':
               Logging._logging(log_file, out)

      if ( p.returncode == 0):
         Logging._logging(log_file, "apply-log - [OK]")
      else:
         Logging._logging(log_file, "apply-log - [ERROR]")
         rb.raise_err(True,3003)


   def _search_qp(self, dir, log_file):
      rb = jbackup_error()
      target = []

      #dir check
      if ( os.path.exists(dir) != True ):
         rb.raise_err(True,3004)

      #target directory
      try:
         os.chdir(dir)
      except Exception as e:
         Logging._logging(log_file, "cannot change directory : " + dir)
         rb.raise_err(True,3005)
      else:
         if (len(glob.glob('*.qp')) == 0):
            Logging._logging(log_file,"Nothing qp file! - d1(ibdata file)")
         else:
            for elem in glob.glob('*.qp'):
               if ( os.path.exists(elem) == True ):
                  target_file = os.getcwd() + '/' + elem
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
               rb.raise_err(True,3005)
            else:
               if (len(glob.glob('*.qp')) == 0):
                  Logging._logging(log_file,"Nothing qp file! - " + str(elem))
               else:
                  for elem in glob.glob('*.qp'):
                     if ( os.path.exists(elem) == True ):
                        target_file = os.getcwd() + '/' + elem
                        self._remove_file(target_file, log_file)


   def _remove_file(self, arg, log_file):
      rb = jbackup_error()
      try:
         os.remove(arg)
      except Exception as e:
         Logging._logging(log_file, "Can not remove qp file - " + arg)
         rb.raise_err(True,3006)
      else:
         Logging._logging(log_file, "removed qp file - " + arg)


   def _exec_decomp(self, applylog_dir, log_file):
      rb = jbackup_error()
      exec_cmd = "innobackupex"
      exec_cmd = exec_cmd + " --decompress "
      exec_cmd = exec_cmd + applylog_dir

      ## print(exec_cmd)

      try:
         p = subprocess.Popen(exec_cmd , shell=True, stderr=subprocess.PIPE)
      except subprocess.CalledProcessError as e:
         Logging._logging(log_file, str(e))
         rb.raise_err(True,3001)
         ## raise SystemExit
      else:
         while True:
            t = p.stderr.readline()
            out = t.decode('utf-8')
            if out == '' and p.poll() != None:
               break
            if out != '':
               Logging._logging(log_file, out)

      if ( p.returncode == 0):
         Logging._logging(log_file, "decompress - [OK]")
      else:
         Logging._logging(log_file, "decompress - [ERROR]")
         rb.raise_err(True,3007)
         ## raise SystemExit

      # remove qp files
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "[Remove qp file]")
      self._search_qp(applylog_dir,log_file)
      Logging._logging_blank(log_file)
      Logging._logging(log_file, "remove qp files - [OK]")

###################################

### END DEF ###
