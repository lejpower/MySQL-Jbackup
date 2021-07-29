#!/usr/bin/python

#######################
### made by Uijun.lee
### DATE 2014-05-20
#######################
import sys
import subprocess

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
    import thread, time
    import os.path
    from jbackup.lib.log.jbackup_logging import Logging
    from jbackup.lib.etc.jbackup_error import jbackup_error
elif(int(version) >= 3):
    import _thread, time
    import os.path
    from jbackup.lib.log.jbackup_logging import Logging
    from jbackup.lib.etc.jbackup_error import jbackup_error

class jbackup_run_backup:
### START DEF ###
   def _exec_backup(self, backup_user , backup_password, backup_host, backup_port, cnf_file, backup_dir, para_cnt, log_file, lock_wait_timeout, lock_wait_threshold, xtra_ver):
      rb = jbackup_error()

      # Options
      ibbackup="xtrabackup"
      comp="--compress"

      exec_cmd = "innobackupex"
      exec_cmd = exec_cmd + " --defaults-file=" + cnf_file
      exec_cmd = exec_cmd + " --host=" + backup_host
      exec_cmd = exec_cmd + " --port=" + backup_port
      exec_cmd = exec_cmd + " --user=" + backup_user
      exec_cmd = exec_cmd + " --password=" + backup_password
      exec_cmd = exec_cmd + " --ibbackup=" + ibbackup
      exec_cmd = exec_cmd + " --compress "
      #if (float(xtra_ver) < 2.0 )
      exec_cmd = exec_cmd + " --lock-wait-timeout=" + str(lock_wait_timeout)
      exec_cmd = exec_cmd + " --lock-wait-threshold=" + str(lock_wait_threshold)
      exec_cmd = exec_cmd + " --slave-info --safe-slave-backup"
      exec_cmd = exec_cmd + " --rsync"
      exec_cmd = exec_cmd + " --parallel=" + str(para_cnt) + " "
      exec_cmd = exec_cmd + backup_dir

      #exec_cmd = ['innobackupex','--host',backup_host,'--port',backup_port,'--user',backup_user,'--password',backup_password]
      #exec_cmd.extend(['--defaults-file',cnf_file,'--ibbackup', ibbackup,'--compress'])
      #exec_cmd.extend(['--lock-wait-timeout',str(lock_wait_timeout),'--lock-wait-threshold',str(lock_wait_threshold)])
      #exec_cmd.extend(['--slave-info','--safe-slave-backup','--parallel', str(para_cnt), backup_dir])

      try:
         p = subprocess.Popen(exec_cmd , shell=True, stderr=subprocess.PIPE)
         #p = subprocess.Popen(exec_cmd, stderr=subprocess.PIPE)
      except subprocess.CalledProcessError as err:
         ## Logging._logging(log_file, "Can not execute Xtrabackup!!!")
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001, log_file)
         ## raise SystemExit
      except Exception as err:
         ## Logging._logging(log_file, "Can not execute Xtrabackup!!!")
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001, log_file)
         ## raise SystemExit
      else:
         while True:
            t = p.stderr.readline()
            out = t.decode('utf-8')
            if out == '' and p.poll() != None:
               break
            ## if p.poll() is None:
               ##time.sleep(0.1)
               ##p.poll()
            if out != '':
               Logging._logging(log_file, out)

      p.wait()
      if ( p.returncode == 0):
         Logging._logging(log_file, "backup - [OK]")
      else:
         Logging._logging(log_file, "backup - [ERROR]")
         rb.raise_err(True,3002, log_file)
         ##raise SystemExit




   def run():
      try:
         p = subprocess.Popen(exec_cmd , shell=True, stderr=subprocess.PIPE)
         #p = subprocess.Popen(exec_cmd, shell=True)
      except subprocess.CalledProcessError as err:
         ## Logging._logging(log_file, "Can not execute Xtrabackup!!!")
         Logging._logging(log_file, str(err))
         rb.raise_err(True,3001)
         ## raise SystemExit
      except Exception as err:
         ## Logging._logging(log_file, "Can not execute Xtrabackup!!!")
         Logging._logging(log_file, str(err))
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
###################################

### END DEF ###
